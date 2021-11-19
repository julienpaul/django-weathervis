# Stdlib imports
import pytest

# Core Django imports
# Third-party app imports
# Imports from my apps
from src.utils import util


def test_is_url():
    """
    GIVEN invalid url (None or empty)
    WHEN  running is_url
    THEN  should return False
    """
    _url = None
    assert util.is_url(_url) is False

    _url = ""
    assert util.is_url(_url) is False

    _url = "thredds/dodsC/metpplatest/met_forecast_1_0km_nordic_latest.nc"
    assert util.is_url(_url) is False

    # Note: no exception raised
    # with pytest.raises(Exception) as execinfo:
    #     util.is_url(_url)


def test_is_url_raises_no_exception():
    """
    GIVEN a valid thredd path to a netcdf input file
    WHEN  running _setupborder
    THEN  raise no Exception
    """
    _url = "https://thredds.met.no/thredds/dodsC/metpplatest/met_forecast_1_0km_nordic_latest.nc"
    try:
        _ = util.is_url(_url)
    except Exception as exc:
        assert False, f"'util.is_url()' raised an exception {exc}"


def test_antipode(geopoint):
    """
    GIVEN a geographic point location
    WHEN  compute the antipode of this point
    THEN
    """
    antipode = util.antipode(geopoint)
    assert geopoint.x != antipode.x
    assert geopoint.y == -antipode.y
    assert geopoint.z == antipode.z


def test_antipode_raises_no_exception(geopoint):
    """
    GIVEN a valid thredd path to a netcdf input file
    WHEN  running _setupborder
    THEN  raise no Exception
    """
    try:
        _ = util.antipode(geopoint)
    except Exception as exc:
        assert False, f"'util.antipode()' raised an exception {exc}"


@pytest.mark.django_db
def test_margin2polygon_raises_no_exception(geopoint, margin):
    """
    GIVEN a valid geopoint location
      and a valid margin
    WHEN  running margin2polygon
    THEN  raise no Exception
    """
    try:
        _lon, _lat, _alt = geopoint.x, geopoint.y, geopoint.z
        _ = util.margin2polygon(_lon, _lat, _alt, margin)
    except Exception as exc:
        assert False, f"'util.antipode()' raised an exception {exc}"
