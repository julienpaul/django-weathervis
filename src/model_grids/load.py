# Stdlib imports
import datetime as dt
import warnings
from pathlib import Path

# Third-party app imports
import geojson
import netCDF4 as nc
import yaml
from dateutil.parser import ParserError
from dateutil.parser import parse as parse_date

# Core Django imports
from django.contrib.gis.utils import LayerMapping
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.utils.timezone import make_aware

# Imports from my apps
from src.utils.util import is_url

from .models import ModelGrid, Variable

model_grid_mapping = {
    "name": "NAME",
    "geom": "MULTIPOLYGON",
    "date_valid_start": "START",
    "date_valid_end": "END",
}

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

    try:
        # reformat dates to isoformat, use TIME_ZONE from settings
        _start = make_aware(parse_date(_start)).isoformat()
        if _end:
            _end = make_aware(parse_date(_end)).isoformat()
        else:
            _end = make_aware(dt.datetime.fromtimestamp(0)).isoformat()

    except ParserError as exc:
        raise ParserError(f"Invalid dates. \n{exc}")

    try:
        with nc.Dataset(_ncfile, "r") as ds:
            # set up border
            _setup_border(ds, name_, _start, _end)
            _save_border(name_, _start)
            # set up and save variables
            _setup_variables(ds, name_, _start)

    except OSError as exc:
        raise OSError(f"Can not find or open file {_ncfile}. \n{exc}")


def _setup_border(ds_, name_, start_, end_):
    """create a geojson of domain's border from the dataset"""
    features = []
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

    # select east border
    east = [(lon[0, x], lat[0, x]) for x in range(m)]
    # select north border
    north = [(lon[x, m - 1], lat[x, m - 1]) for x in range(n)]
    # select west border
    west = [(lon[n - 1, x], lat[n - 1, x]) for x in reversed(range(m))]
    # select south border
    south = [(lon[x, 0], lat[x, 0]) for x in reversed(range(n))]

    points_list = [*east, *north, *west, *south]

    border = geojson.Polygon([points_list])

    # add features...
    _prop = {
        "NAME": name_,
        "START": start_,
        "END": end_,
    }
    features.append(geojson.Feature(geometry=border, properties=_prop))

    # create json file
    feature_collection = geojson.FeatureCollection(features)

    output = model_grid_data_path / (name_ + ".geojson")
    model_grid_data_path.mkdir(parents=True, exist_ok=True)
    with open(output, "w") as f:
        geojson.dump(feature_collection, f)


def _save_border(name_, start_, verbose=False):
    """save shape file in database"""
    if not name_:
        raise TypeError(f"Invalid type for argument name_ -{type(name_)}-")

    geojson = model_grid_data_path / (name_ + ".geojson")
    if not geojson.exists():
        raise OSError(f"Geojson file {geojson} does not exist")

    lm = LayerMapping(
        ModelGrid,
        str(geojson),
        model_grid_mapping,
        transform=False,
    )

    try:
        lm.save(strict=True, verbose=verbose, silent=True)
    except IntegrityError:
        warnings.warn(f"ModelGrid ({name_}, {start_}) already exists.")


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
