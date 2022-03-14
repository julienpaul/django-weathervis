# Stdlib imports
from pathlib import Path

# Third-party app imports
import yaml

# Core Django imports
from django.contrib.gis.geos import Point as geoPoint

# Imports from my apps
from src.margins.models import Margin
from src.utils import util

from .models import Station

station_path = Path(__file__).resolve().parent
station_data_path = station_path / "data"


class MyDumper(yaml.SafeDumper):
    # HACK: insert blank lines between top-level objects
    # inspired by https://stackoverflow.com/a/44284819/3786245
    def write_line_break(self, data=None):
        super().write_line_break(data)

        if len(self.indents) == 1:
            super().write_line_break()


def _check_param(dict_, fparam_):
    """
    check dictionary elements and reformat if need be
    """
    if not isinstance(dict_, dict):
        raise TypeError(f"{fparam_} must be a dictionnary.")
    else:
        for key, v in dict_.items():
            if not isinstance(v, dict):
                raise TypeError(
                    f"Value of key '{key}' must be a dictionnary. See {fparam_}."
                )

            if "margin" in v:
                if not isinstance(v["margin"], dict):
                    raise TypeError(
                        f"Value of '{key}['margin']' must be a dictionnary. See {fparam_}."
                    )


def upload(fparam_=station_data_path / "stations.ini.yaml"):
    """upload and save station and margin"""
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

    _default = param.get("default", {})
    _margin = _default.get("margin", {})
    for key, dic in param.items():
        if key == "default":
            # do nothing
            continue

        margin = dic.get("margin", {})
        # voir setdefault instead of get
        m, created = Margin.objects.get_or_create(
            west=margin.get("west", _margin.get("west")),
            east=margin.get("east", _margin.get("east")),
            north=margin.get("north", _margin.get("north")),
            south=margin.get("south", _margin.get("south")),
        )

        lon = float(dic.get("lon", _default.get("lon", 0)))
        lat = float(dic.get("lat", _default.get("lat", 0)))
        alt = float(dic.get("height", _default.get("height", 0)))
        geom = geoPoint(lon, lat, alt)
        margin_geom = util.margin2polygon(lon, lat, alt, m)

        s, created = Station.objects.get_or_create(
            name=key,
            geom=geom,
            station_id=dic.get("stationID", _default.get("stationID")),
            wmo_id=dic.get("WMOID", _default.get("WMOID")),
            description=dic.get("description", _default.get("description", "")),
            margin=m,
            margin_geom=margin_geom,
        )


def download(fparam_=station_data_path / "stations.yaml"):
    """download station and margin from database and write station.yaml

    Note: only active stations are downloaded.
    """
    dic = {}
    for station in Station.objects.all():
        if station.is_active:
            dic[station.name] = {
                "lat": station.latitude,
                "lon": station.longitude,
                "height": station.altitude,
                "stationID": station.station_id,
                "WMOID": station.wmo_id,
                "description": station.description,
                "margin": {
                    "west": float(station.margin.west),
                    "east": float(station.margin.east),
                    "north": float(station.margin.north),
                    "south": float(station.margin.south),
                },
            }

    header = """
# <location name>:
#   lat: <location latitude (degree_north)>
#   lon: <location longitude (degree_east)>
#   height: <location height ()>
#   stationId: <station identifier>
#   WMOID:     <WMO identifier>
#   description: >
#     <description could be write on multilines>
#   margin: <create box around location to display>
#     north:  <adds X degree(s) north of location (degree)>
#     east:   <adds X degree(s) east of location (degree)>
#     south:  <substracts X degree(s) south of location (degree)>
#     west:   <substracts X degree(s) west of location (degree)>
"""

    with open(fparam_, "w") as stream:
        stream.write(header + "\n")
        yaml.dump(
            dic,
            stream=stream,
            Dumper=MyDumper,
            default_flow_style=False,
            sort_keys=False,
            indent=4,
        )

    header = """rel_begin_YYYYMMDD;rel_begin_HHMMSS;rel_end_YYYYMMDD;rel_end_HHMMSS;\
        rel_min_1;rel_min_2;rel_max_1;rel_max_2;rel_ZTYPE;rel_ZPOINT_1;rel_ZP OINT_2;\
        rel_NUMB_PART;rel_XMASS;rel_domain_name;rel_lon;rel_lat;number_grid"""
    with open(station_data_path / "releases.csv", "w") as stream:
        stream.write(header + "\n")
        for _name, _dic in dic.items():
            stream.write(
                f"NaN;NaN;NaN;NaN;NaN;NaN;NaN;NaN;1;0;2000;100000;100;{_name};NaN;NaN;200"
                + "\n"
            )
