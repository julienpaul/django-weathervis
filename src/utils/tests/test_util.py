# Stdlib imports
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
