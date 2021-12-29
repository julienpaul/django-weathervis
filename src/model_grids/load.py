# Stdlib imports
from pathlib import Path

# Third-party app imports
import geojson
import netCDF4 as nc
import yaml

# Core Django imports
from django.contrib.gis.utils import LayerMapping

# Imports from my apps
from src.utils.util import is_url

from .models import ModelGrid

model_grid_mapping = {
    "name": "NAME",
    "geom": "MULTIPOLYGON",
}

model_grid_path = Path(__file__).resolve().parent
model_grid_data_path = model_grid_path / "data"


def _setup_border(name_, ncfile_):
    """create a geojson of domain's border from the netcdf file"""
    features = []
    if not name_:
        raise TypeError(f"Invalid type for argument name_ -{type(name_)}-")

    try:
        with nc.Dataset(ncfile_, "r") as ds:
            for v in ["latitude", "longitude"]:
                if v not in ds.variables:
                    raise IndexError(f"Can not find variable '{v}' in file '{ncfile_}'")
                # check lat, lon 2D
                if ds.variables[v].ndim != 2:
                    raise TypeError(f"Invalid dimension for variable {v}. Must be 2D.")

            # read lat,lon variable
            lat = ds.variables["latitude"][:]
            lon = ds.variables["longitude"][:]

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
        features.append(geojson.Feature(geometry=border, properties={"NAME": name_}))

        # create json file
        feature_collection = geojson.FeatureCollection(features)

        output = model_grid_data_path / (name_ + ".geojson")
        model_grid_data_path.mkdir(parents=True, exist_ok=True)
        with open(output, "w") as f:
            geojson.dump(feature_collection, f)

    except OSError as exc:
        raise OSError(f"Can not find or open file {ncfile_}. {exc}")


def _save(name_, verbose=True):
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
    lm.save(strict=True, verbose=verbose)


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
            # check url or file
            if not (is_url(v) or (Path(v).is_file and Path(v).exists())):
                raise ValueError(
                    f"'data[{k}]' in {fparam_} must be an url or an existing file."
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
            f"Something goes wrong when uploading extra parameters file -{fparam_}-. {exc}"
        )

    for key, val in param["data"].items():
        _setup_border(key, val)
        _save(key)
