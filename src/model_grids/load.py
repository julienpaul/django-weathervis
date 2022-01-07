# Stdlib imports
import datetime as dt
from pathlib import Path

# Third-party app imports
import netCDF4 as nc
import yaml
from dateutil.parser import ParserError
from dateutil.parser import parse as parse_date

# Core Django imports
from django.contrib.gis.geos import LinearRing
from django.contrib.gis.geos import Polygon as geoPolygon
from django.core.exceptions import ObjectDoesNotExist
from django.utils.timezone import make_aware

# Imports from my apps
from src.utils.util import is_url

from .models import ModelGrid, Variable

model_grid_path = Path(__file__).resolve().parent
model_grid_data_path = model_grid_path / "data"


def _setup_grid(name_, dict_):
    """create ModelGrid instance from the netcdf file
    and save it in database.
    """
    if not name_:
        raise TypeError(f"Invalid type for argument name_ -{type(name_)}-")

    _ncfile = dict_.get("url")
    _start = dict_.get("date_valid_start")
    _end = dict_.get("date_valid_end")
    _leadtime = dict_.get("leadtime")

    try:
        with nc.Dataset(_ncfile, "r") as ds:
            # set up border
            _setup_border(ds, name_, _start, _end, _leadtime)
            # set up and save variables
            _setup_variables(ds, name_, _start)

    except OSError as exc:
        raise OSError(f"Can not find or open file {_ncfile}. \n{exc}")


def _get_leadtime(ds_, leadtime_=None):
    """read leadtime from ncfile if not in yaml file"""
    if not leadtime_:
        try:
            time_var = ds_.variables["time"]
            dtime = nc.num2date(time_var[:], time_var.units)
            tdelta = dtime[-1] - dtime[0]
        except Exception as exc:
            raise Exception(
                f"Something goes wrong when reading time in file -{ds_.name}-."
                f"\n{exc}"
            )
    else:
        try:
            tdelta = dt.timedelta(hours=leadtime_)
        except Exception as exc:
            raise Exception(
                f"Something goes wrong when converting leadtime -{leadtime_}- to timedelta."
                f"\n{exc}"
            )

    return tdelta


def _setup_border(ds_, name_, start_, end_, leadtime_=None):
    """create a geojson of domain's border from the dataset"""
    # set up border
    for v in ["latitude", "longitude"]:
        if v not in ds_.variables:
            raise IndexError(f"Can not find variable '{v}' in dataset '{ds_.name}'")
        # check lat, lon 2D
        if ds_.variables[v].ndim != 2:
            raise TypeError(f"Invalid dimension for variable {v}. Must be 2D.")

    # read lat,lon variable
    lat = ds_.variables["latitude"][:]
    lon = ds_.variables["longitude"][:]

    n, m = lat.shape
    alt = 0

    # select east border
    east = [(lon[0, x], lat[0, x], alt) for x in range(m)]
    # select north border
    north = [(lon[x, m - 1], lat[x, m - 1], alt) for x in range(n)]
    # select west border
    west = [(lon[n - 1, x], lat[n - 1, x], alt) for x in reversed(range(m))]
    # select south border
    south = [(lon[x, 0], lat[x, 0], alt) for x in reversed(range(n))]

    points_list = [*east, *north, *west, *south]

    # border = geojson.Polygon([points_list])
    border = geoPolygon(LinearRing(points_list))

    try:
        # reformat dates to isoformat, use TIME_ZONE from settings
        start = make_aware(parse_date(start_)).isoformat()
        if end_:
            end = make_aware(parse_date(end_)).isoformat()
        else:
            end = make_aware(dt.datetime.fromtimestamp(0)).isoformat()

    except ParserError as exc:
        raise ParserError(f"Invalid dates. \n{exc}")

    # check 'time' variable
    for v in ["time"]:
        if v not in ds_.variables:
            raise IndexError(f"Can not find variable '{v}' in dataset '{ds_.name}'")
        else:
            list_v = ds_.get_variables_by_attributes(standard_name="time")
            if len(list_v) != 1:
                raise ValueError(
                    f"Do not find only one variable with standard name 'time'"
                    f" in dataset '{ds_.name}'."
                )
            else:
                # overwrite with right variable name for 'time'
                v = list_v[0].name
        # check lat, lon 2D
        if ds_.variables[v].ndim != 1:
            raise TypeError(f"Invalid dimension for variable {v}. Must be 1D.")

        if not ds_.dimensions[ds_.variables[v].dimensions[0]].isunlimited():
            raise TypeError(
                f"Invalid dimension for time variable -{v}-. Must be 'unlimited'."
            )

    if not leadtime_:
        leadtime = None

    # read and convert to timedelta
    leadtime = _get_leadtime(ds_, leadtime_)

    # save ModelGrid
    s, created = ModelGrid.objects.get_or_create(
        name=name_,
        geom=border,
        date_valid_start=start,
        date_valid_end=end,
        leadtime=leadtime,
    )


def _setup_variables(ds_, name_, start_):
    """create Variable instances for each variables from the dataset,
    and save them in database.
    """
    try:
        mg = ModelGrid.objects.get(
            name=name_,
            date_valid_start=start_,
        )
        for k, v in ds_.variables.items():
            var, created = Variable.objects.get_or_create(
                name=k,
                model_grid=mg,
            )
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist(f"ModelGrid ({name_}, {start_}) does not exist.")


def _check_param(dict_, fparam_):
    """
    check dictionary elements and reformat if need be
    """

    if "data" not in dict_:
        raise KeyError(f"No key 'data' in {fparam_}.")
    elif not isinstance(dict_["data"], dict):
        raise TypeError(f"Value of key 'data' in {fparam_} must be a dictionnary.")
    else:
        for k, v in dict_["data"].items():
            # check keys
            for kk in ["url", "date_valid_start"]:
                # do not check "date_valid_end", as it could be omitted
                if kk not in v:
                    raise KeyError(f"key -{kk}- is missing for model grid {k}")
            # check url or file
            _url = v.get("url")
            if not (is_url(_url) or (Path(_url).is_file and Path(_url).exists())):
                raise ValueError(
                    f"Invalid URL for model grid {k}, must be an url or an existing file."
                    f"\nCheck {fparam_}"
                )
            # check dates
            for _d in ["date_valid_start", "date_valid_end"]:
                _date = v.get(_d)

                try:
                    if _date or _d != "date_valid_end":
                        _ = parse_date(_date)
                except Exception:
                    raise ValueError(
                        f"Invalid datetime format -{_date}- for key {_d} for model grid {k}; "
                        f"\nCheck {fparam_}"
                    )


def up(fparam_=model_grid_path / "data.yaml"):
    """upload and save shape file of weather forecast models"""
    try:
        # read parameters configuration file yaml
        with open(fparam_, "r") as stream:
            try:
                param = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                raise yaml.YAMLError(exc)

        # check parameters file
        _check_param(param, fparam_)

    except Exception as exc:
        raise Exception(
            f"Something goes wrong when uploading extra parameters file -{fparam_}-."
            f"\n{exc}"
        )

    for key, val in param["data"].items():
        _setup_grid(key, val)
