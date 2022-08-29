# Stdlib imports
from pathlib import Path

# Third-party app imports
import yaml

# Core Django imports
from django.contrib.gis.geos import Polygon as GeoPolygon

# Imports from my apps
from src.campaigns.models import Campaign
from src.stations.util import MyDumper

from .models import Domain

domain_path = Path(__file__).resolve().parent
domain_data_path = domain_path / "data"


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


def upload(fparam_=domain_data_path / "domains.ini.yaml"):
    """upload and save domain"""
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
    for key, dic in param.items():
        if key == "default":
            # do nothing
            continue

        west = float(dic.get("west", _default.get("west", 0)))
        north = float(dic.get("north", _default.get("north", 0)))
        east = float(dic.get("east", _default.get("east", 0)))
        south = float(dic.get("south", _default.get("south", 0)))
        alt = float(dic.get("height", _default.get("height", 0)))

        coords = (
            (west, north, alt),
            (east, north, alt),
            (east, south, alt),
            (west, south, alt),
            (west, north, alt),
        )
        geom = GeoPolygon(coords)

        s, created = Domain.objects.get_or_create(
            name=key,
            geom=geom,
            description=dic.get("description", _default.get("description", "")),
        )


def download(fparam_=domain_data_path / "domains.yaml"):
    """download domain from database and write domains.yaml

    Note:
        - only active domains are downloaded.
        - only domains from the active campaign are downloaded.
    """
    dic = {}
    _pk = Domain.objects.all().first().active_campaign
    if _pk:
        campaign = Campaign.objects.get(pk=_pk)
    else:
        campaign = "any or none"

    for domain in Domain.objects.all():
        if domain.is_active and (
            not domain.active_campaign
            or domain.active_campaign
            in domain.campaigns.all().values_list("id", flat=True)
        ):
            dic[domain.name] = {
                "west": domain.west,
                "north": domain.north,
                "east": domain.east,
                "south": domain.south,
                "height": domain.altitude,
                "description": domain.description,
                "plots": [p.name for p in domain.plots.all()],
            }

    header = f"""
#
# Domains from campaign "{campaign}"
# ------
# <domain name>:
#   north: <domain latitude north (degree_north)>
#   south: <domain latitude south (degree_north)>
#   west: <domain longitude west (degree_east)>
#   east: <domain longitude east (degree_east)>
#   height: <domain height (m)>
#   description: >
#     <description could be write on multilines>
#   plots: list of plots selected fot this domain
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
