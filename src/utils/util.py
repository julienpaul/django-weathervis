# Stdlib imports
from urllib.parse import urlparse

# Third-party app imports
import yaml

# Core Django imports
from django.conf import settings
from django.contrib.gis.geos import Point as GeoPoint
from django.contrib.gis.geos import Polygon as GeoPolygon

# Imports from my apps

degree_sign = "\N{DEGREE SIGN}"


def margin2polygon(lon, lat, alt, margin):
    """compute Polygon geometry for these coordinates and Margin[summary]

    Args:
        lon ([type]): [description]
        lat ([type]): [description]
        alt ([type]): [description]
        margin (Margin): [description]

    Returns:
        [type]: [description]
    """
    minlon = float(lon) - float(margin.west)
    maxlon = float(lon) + float(margin.east)
    minlat = float(lat) - float(margin.south)
    maxlat = float(lat) + float(margin.north)

    ll = GeoPoint(minlon, minlat, alt)
    ul = GeoPoint(minlon, maxlat, alt)
    ur = GeoPoint(maxlon, maxlat, alt)
    lr = GeoPoint(maxlon, minlat, alt)

    polygon = GeoPolygon([ll, ul, ur, lr, ll])

    return polygon


def is_url(url_):
    """
    check if argument is an url

    :param url_: string of url to check

    :return: boolean
    """
    try:
        result = urlparse(url_)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def antipode(pnt_: GeoPoint):
    """compute antipode point coordinates

    Args:
        pnt_ ([Point]): 3D coordinates
    """
    lon = pnt_.x + 180
    lat = -pnt_.y

    # longitude between -180, 180
    lon = (lon % 360 + 540) % 360 - 180

    return GeoPoint(lon, lat, pnt_.z)


def read_subtext_file(fparam_=None):
    """read subtext file"""
    try:
        if fparam_ is None:
            fparam_ = "/".join([settings.STATIC_ROOT, "yaml", "plots", "subtext.yaml"])
        # read parameters configuration file yaml
        with open(fparam_, "r") as stream:
            try:
                param = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                raise yaml.YAMLError(exc)
        # check parameters file
        return param
    except Exception as exc:
        raise Exception(
            f"Something goes wrong when getting subtext of VerticalMeteogram. See parameters file -{fparam_}-. {exc}"
        )
