# Stdlib imports
import numpy as np
import pytest
import xarray as xr

# Core Django imports
# Third-party app imports
import yaml
from faker import Faker

# Imports from my apps
from src.weather_forecast import load
from src.weather_forecast.models import WeatherForecastBorder

pytestmark = pytest.mark.django_db
# TODO: use smaller data/create small fake data to speed up tests


def fake_geonc(tmp_path, lat_name="lat", lon_name="lon"):
    """
    create dummy netcdf file with 1D longitude and latitude.

    tmp_path: path to repository where file will be created
    lat_name: output variable name for latitude
    lon_name: output variable name for longitude
    return: path of the file
    """
    _tmp = tmp_path / "test.nc"

    fake = Faker()
    lat, lon = [], []
    for _ in range(3):
        lon.append(fake.longitude())
        lat.append(fake.latitude())
    #
    lon = np.array(lon, dtype="float")
    lat = np.array(lat, dtype="float")

    ds = xr.Dataset(
        coords={
            lon_name: (["x"], lon),
            lat_name: (["y"], lat),
        },
    )
    ds.to_netcdf(path=_tmp, format="NETCDF4_CLASSIC")

    return _tmp


def test__setup_border_invalid_name():
    """
    GIVEN invalid name (None or empty)
    WHEN  running _setupborder
    THEN  raise TypeError
     with error message starting with 'Invalid type for argument'
    """

    with pytest.raises(TypeError) as execinfo:
        load._setup_border("", "")
        load._setup_border(None, "")
        load._setup_border(" ", "")
    # check error message
    assert str(execinfo.value).startswith("Invalid type for argument name_")


def test__setup_border_invalid_ncfile(weatherForecastBorder: WeatherForecastBorder):
    """
    GIVEN invalid netcdf file input (None or empty)
    WHEN  running _setupborder
    THEN  raise OSError
     with error message starting with 'Can not find or open file'
    """

    with pytest.raises(OSError) as execinfo:
        load._setup_border(weatherForecastBorder.name, "")
        load._setup_border(weatherForecastBorder.name, None)
        thredd = "https://thredds.met.no/thredds/dodsC/metpplatest/met_forecast_1_0km_nordic_latestt.nc"
        load._setup_border(weatherForecastBorder.name, thredd)
    # check error message
    assert str(execinfo.value).startswith("Can not find or open file")


def test__setup_border_variable_not_found(tmp_path):
    """
    GIVEN a netcdf input file with missing variable 'latitude' or 'longitude'
    WHEN  running _setupborder
    THEN  raise IndexError
     with error message starting with 'Can not find variable'
    """
    # create dummy netcdf file
    _tmp = fake_geonc(tmp_path)

    with pytest.raises(IndexError) as execinfo:
        load._setup_border("test", _tmp)
    # check error message
    assert str(execinfo.value).startswith("Can not find variable")


def test__setup_border_variable_not_2D(tmp_path):
    """
    GIVEN a netcdf input file
     with 1D variables of 'latitude' or 'longitude'
    WHEN  running _setupborder
    THEN  raise IndexError
     with error message starting with 'Can not find variable'
    """
    # create dummy netcdf file
    _tmp = fake_geonc(tmp_path, lat_name="latitude", lon_name="longitude")

    with pytest.raises(TypeError) as execinfo:
        load._setup_border("test", _tmp)
    # check error message
    assert str(execinfo.value).startswith("Invalid dimension for variable")


def test__setup_border_geojson_created(weatherForecastBorder: WeatherForecastBorder):
    """
    GIVEN a valid thredd path to a netcdf input file
    WHEN  running _setupborder
    THEN  a 'geojson' file must have been created in the right directory
    """

    thredd = "https://thredds.met.no/thredds/dodsC/metpplatest/met_forecast_1_0km_nordic_latest.nc"
    load._setup_border(weatherForecastBorder.name, thredd)
    # check directory
    assert load.weather_forecast_data_path.exists()
    assert load.weather_forecast_data_path.is_dir()
    # check geojson file
    output = load.weather_forecast_data_path / (weatherForecastBorder.name + ".geojson")
    assert output.exists()
    assert output.is_file()

    # clean directory
    output.unlink()


def test__setup_border_raises_no_exception():
    """
    GIVEN a valid thredd path to a netcdf input file
    WHEN  running _setupborder
    THEN  raise no Exception
    """
    thredd = "https://thredds.met.no/thredds/dodsC/metpplatest/met_forecast_1_0km_nordic_latest.nc"
    try:
        load._setup_border("test", thredd)
    except Exception as exc:
        assert False, f"'load._save()' raised an exception {exc}"

    # clean directory
    output = load.weather_forecast_data_path / ("test" + ".geojson")
    output.unlink()


def test__save_invalid_name():
    """
    GIVEN invalid name (None or empty)
    WHEN  running _save
    THEN  raise TypeError
     with error message starting with 'Invalid type for argument'
    """

    with pytest.raises(TypeError) as execinfo:
        load._save("")
        load._save(None)
        load._save(" ")
    # check error message
    assert str(execinfo.value).startswith("Invalid type for argument name_")


def test__save_invalid_geojson(weatherForecastBorder: WeatherForecastBorder):
    """
    GIVEN a name, not associated to a geojson file
    WHEN  running _save
    THEN  raise OSError
     with error message starting with 'Geojson file' ending with 'does not exist'
    """

    with pytest.raises(OSError) as execinfo:
        load._save(weatherForecastBorder.name)
    # check error message
    assert str(execinfo.value).startswith("Geojson file")
    assert str(execinfo.value).endswith("does not exist")


def test__save_add_to_db():
    """
    GIVEN a name associated to a valid geojson file
    WHEN  running _save
    THEN  should create an object in the database
    """
    thredd = "https://thredds.met.no/thredds/dodsC/metpplatest/met_forecast_1_0km_nordic_latest.nc"
    load._setup_border("test", thredd)
    load._save("test")
    # clean directory
    output = load.weather_forecast_data_path / ("test" + ".geojson")
    output.unlink()

    all_entries = WeatherForecastBorder.objects.all()

    # one element on database
    assert len(all_entries) == 1
    assert all_entries[0].name == "test"


def test__save_raises_no_exception():
    """
    GIVEN a name associated to a valid geojson file
    WHEN  running _save
    THEN  raise no Exception
    """
    thredd = "https://thredds.met.no/thredds/dodsC/metpplatest/met_forecast_1_0km_nordic_latest.nc"
    load._setup_border("test", thredd)
    try:
        load._save("test")
    except Exception as exc:
        assert False, f"'load._save()' raised an exception {exc}"

    # clean directory
    output = load.weather_forecast_data_path / ("test" + ".geojson")
    output.unlink()


def test__check_param_data_key():
    """
    GIVEN a dictionary with no key 'data'
    WHEN  checking it
    THEN  raise KeyError
     with error message starting with "No key 'data' in"
    """
    dict = {"dat": "something"}
    with pytest.raises(KeyError) as execinfo:
        load._check_param(dict, "whatever")
    # check error message
    assert "No key 'data' in" in str(execinfo.value)
    # TODO: find why the line below do not work ?
    # assert str(execinfo.value).startswith("No key 'data' in")


def test__check_param_data_value():
    """
    GIVEN a dictionary
     with 'data' key's value which is not a dictionary
    WHEN  checking it
    THEN  raise TypeError
     with error message "'data' in whatever must be a dictionnary."
    """
    dict = {"data": "something"}
    with pytest.raises(TypeError) as execinfo:
        load._check_param(dict, "whatever")
    # check error message
    assert str(execinfo.value).startswith("Value of key 'data' in")
    assert str(execinfo.value).endswith("must be a dictionnary.")

    dict = {"data": ["something", "something else"]}
    with pytest.raises(TypeError) as execinfo:
        load._check_param(dict, "whatever")
    # check error message
    assert str(execinfo.value).startswith("Value of key 'data' in")
    assert str(execinfo.value).endswith("must be a dictionnary.")


def test__check_param_data_url():
    """
    GIVEN a dictionary
     with 'data' key's value which is a dictionary
     with a value which is an invalid thredd path or file
    WHEN  checking it
    THEN  raise TypeError
     with error message "'data' in whatever must be a dictionnary."
    """
    thredd = "thredds/dodsC/metpplatest/met_forecast_1_0km_nordic_latest.nc"
    dict = {"data": {"thredd": thredd}}
    with pytest.raises(ValueError) as execinfo:
        load._check_param(dict, "whatever")
    # check error message
    assert str(execinfo.value).endswith("must be an url or an existing file.")


def test__check_param_raises_no_exception():
    """
    GIVEN a dictionary
     with 'data' key's value which is a dictionary
     with a value which is an valid thredd path or file
    WHEN  checking it
    THEN  raise no Exception
    """
    thredd = "https://thredds.met.no/thredds/dodsC/metpplatest/met_forecast_1_0km_nordic_latest.nc"
    dict = {"data": {"thredd": thredd}}
    try:
        load._check_param(dict, "whatever")
    except Exception as exc:
        assert False, f"'load._check_param()' raised an exception {exc}"


def test_run_yaml(tmp_path):
    """
    GIVEN an invalid yaml input file
    WHEN  running run
    THEN  raise Exception
     with error message starting with 'Something goes wrong when loading extra parameters file'
    """
    _tmp = None
    with pytest.raises(Exception) as execinfo:
        load.run(_tmp)

    # check error message
    assert str(execinfo.value).startswith(
        "Something goes wrong when loading extra parameters"
    )

    dict = {"data": "something"}
    _tmp = tmp_path / "meta.yaml"
    with open(_tmp, "w+") as ff:
        yaml.dump(dict, ff, allow_unicode=True, default_flow_style=False)

    with pytest.raises(Exception) as execinfo:
        load.run(_tmp)


def test_run_raises_no_exception():
    """
    GIVEN an valid yaml input file
    WHEN  running run
    THEN  raise no Exception
    """
    """
    Assert your python code raises no exception.
    """
    try:
        load.run()
    except Exception as exc:
        assert False, f"'load.run()' raised an exception {exc}"


@pytest.mark.skip(reason="useless ??")
def test_run_yaml_success():
    """
    GIVEN an valid yaml input file
    WHEN  running run
    THEN  'geojosn' file(s) created on load.weather_forecast_data_path
     and  element(s) added to the database
    """
    load.run()
    fparam_ = load.weather_forecast_path / "data.yaml"
    with open(fparam_, "r") as stream:
        try:
            param = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    # check geojson exist
    for f in param["data"].keys():
        output = load.weather_forecast_data_path / (f + ".geojson")
        assert output.exists()
        assert output.is_file()
    # check instance on database
    all_entries = WeatherForecastBorder.objects.all()

    # all elements on database
    assert len(all_entries) == len(param["data"])
