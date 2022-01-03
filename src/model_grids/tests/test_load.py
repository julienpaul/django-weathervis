# Stdlib imports
import datetime as dt

# Core Django imports
# Third-party app imports
import netCDF4 as nc
import numpy as np
import pytest
import xarray as xr
import yaml
from dateutil.parser import ParserError
from faker import Faker

# Imports from my apps
from src.model_grids import load
from src.model_grids.models import ModelGrid

pytestmark = pytest.mark.django_db
# TODO: use smaller data/create small fake data to speed up tests


def fake_geonc(tmp_path, lat_name="lat", lon_name="lon", alt_name="alt"):
    """
    create dummy netcdf file with 1D longitude and latitude.

    tmp_path: path to repository where file will be created
    lat_name: output variable name for latitude
    lon_name: output variable name for longitude
    return: path of the file
    """
    _tmp = tmp_path / "test.nc"

    fake = Faker()
    lat, lon, alt = [], [], []
    for _ in range(3):
        lon.append(fake.longitude())
        lat.append(fake.latitude())
        alt.append(fake.pyfloat(positive=True, max_value=99999))
    #
    lon = np.array(lon, dtype="float")
    lat = np.array(lat, dtype="float")
    alt = np.array(alt, dtype="float")

    ds = xr.Dataset(
        coords={
            lon_name: (["x"], lon),
            lat_name: (["y"], lat),
            alt_name: (["z"], alt),
        },
    )
    ds.to_netcdf(path=_tmp, format="NETCDF4_CLASSIC")

    return _tmp


def test__setup_border_variable_not_found(tmp_path):
    """
    GIVEN a netcdf input file with missing variable 'latitude' or 'longitude'
    WHEN  running _setupborder
    THEN  raise IndexError
     with error message starting with 'Can not find variable'
    """
    # create dummy netcdf file
    _tmp = fake_geonc(tmp_path)
    _name = "test"
    _start = "2021-01-01"
    _end = _start

    ds = nc.Dataset(_tmp, "r")

    with pytest.raises(IndexError) as execinfo:
        load._setup_border(ds, _name, _start, _end)
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
    _name = "test"
    _start = "2021-01-01"
    _end = _start

    ds = nc.Dataset(_tmp, "r")

    with pytest.raises(TypeError) as execinfo:
        load._setup_border(ds, _name, _start, _end)
    # check error message
    assert str(execinfo.value).startswith("Invalid dimension for variable")


def test__setup_border_geojson_created(modelGrid: ModelGrid):
    """
    GIVEN a valid thredd path to a netcdf input file
    WHEN  running _setupborder
    THEN  a 'geojson' file must have been created in the right directory
    """

    thredd = "https://thredds.met.no/thredds/dodsC/metpplatest/met_forecast_1_0km_nordic_latest.nc"
    _start = "2021-01-01"
    _end = _start

    ds = nc.Dataset(thredd, "r")

    load._setup_border(ds, modelGrid.name, _start, _end)
    # check directory
    assert load.model_grid_data_path.exists()
    assert load.model_grid_data_path.is_dir()
    # check geojson file
    output = load.model_grid_data_path / (modelGrid.name + ".geojson")
    assert output.exists()
    assert output.is_file()

    # clean directory
    output.unlink()


def test__setup_border_raises_no_exception(tmp_path):
    """
    GIVEN a valid
    WHEN  running _setup_grid
    THEN  raise no Exception
    """
    thredd = "https://thredds.met.no/thredds/dodsC/metpplatest/met_forecast_1_0km_nordic_latest.nc"
    _name = "test"
    _start = "2021-01-01"
    _end = _start

    ds = nc.Dataset(thredd, "r")

    try:
        # set up border
        load._setup_border(ds, _name, _start, _end)
    except Exception as exc:
        assert False, f"'load._setup_border()' raised an exception {exc}"


def test__setup_grid_invalid_date():
    """
    GIVEN a invalid date
    WHEN  running _setup_grid
    THEN  raise TypeError
    """
    thredd = "https://thredds.met.no/thredds/dodsC/metpplatest/met_forecast_1_0km_nordic_latest.nc"
    dict = {"url": thredd, "date_valid_start": "2020-13-01"}
    with pytest.raises(ParserError) as execinfo:
        load._setup_grid("test", dict)

    # check error message
    assert str(execinfo.value).startswith("Invalid dates.")


def test__setup_grid_invalid_ncfile(modelGrid: ModelGrid):
    """
    GIVEN invalid netcdf file input (None or empty)
    WHEN  running _setup_grid
    THEN  raise OSError
     with error message starting with 'Can not find or open file'
    """

    with pytest.raises(OSError) as execinfo:
        dict = {"url": "", "date_valid_start": "2020-01-01"}
        load._setup_grid(modelGrid.name, dict)
        dict = {"url": None, "date_valid_start": "2020-01-01"}
        load._setup_grid(modelGrid.name, dict)
        thredd = "https://thredds.met.no/thredds/metpplatest/met_forecast_1_0km_nordic_latestt.nc"
        dict = {"url": thredd, "date_valid_start": "2020-01-01"}
        load._setup_grid(modelGrid.name, dict)
    # check error message
    assert str(execinfo.value).startswith("Can not find or open file")


def test__setup_grid_invalid_name():
    """
    GIVEN a invalid name
    WHEN  running _setup_grid
    THEN  raise TypeError
    """
    thredd = "https://thredds.met.no/thredds/dodsC/metpplatest/met_forecast_1_0km_nordic_latest.nc"
    dict = {"url": thredd, "date_valid_start": "2020-01-01"}
    with pytest.raises(TypeError) as execinfo:
        load._setup_grid(None, dict)
        load._setup_grid("", dict)
        load._setup_grid(" ", dict)
    # check error message
    assert str(execinfo.value).startswith("Invalid type for argument name_")


def test__setup_grid_raises_no_exception():
    """
    GIVEN a valid
    WHEN  running _setup_grid
    THEN  raise no Exception
    """
    thredd = "https://thredds.met.no/thredds/dodsC/metpplatest/met_forecast_1_0km_nordic_latest.nc"
    dict = {"url": thredd, "date_valid_start": "2020-01-01"}
    try:
        load._setup_grid("test", dict)
    except Exception as exc:
        assert False, f"'load._setup_grid()' raised an exception {exc}"

    # clean directory
    output = load.model_grid_data_path / ("test" + ".geojson")
    output.unlink()


def test__save_border_invalid_name():
    """
    GIVEN invalid name (None or empty)
    WHEN  running _save
    THEN  raise TypeError
     with error message starting with 'Invalid type for argument'
    """
    _start = dt.datetime.fromtimestamp(0).isoformat()

    with pytest.raises(TypeError) as execinfo:
        load._save_border("", _start)
        load._save_border(None, _start)
        load._save_border(" ", _start)
    # check error message
    assert str(execinfo.value).startswith("Invalid type for argument name_")


def test__save_border_invalid_geojson(modelGrid: ModelGrid):
    """
    GIVEN a name, not associated to a geojson file
    WHEN  running _save
    THEN  raise OSError
     with error message starting with 'Geojson file' ending with 'does not exist'
    """
    _start = dt.datetime.fromtimestamp(0).isoformat()

    with pytest.raises(OSError) as execinfo:
        load._save_border(modelGrid.name, _start)
    # check error message
    assert str(execinfo.value).startswith("Geojson file")
    assert str(execinfo.value).endswith("does not exist")


def test__save_border_add_to_db():
    """
    GIVEN a name associated to a valid geojson file
    WHEN  running _save
    THEN  should create an object in the database
    """
    thredd = "https://thredds.met.no/thredds/dodsC/metpplatest/met_forecast_1_0km_nordic_latest.nc"
    _name = "test"
    _start = dt.datetime.fromtimestamp(0).isoformat()
    _end = _start

    ds = nc.Dataset(thredd, "r")

    load._setup_border(ds, _name, _start, _end)
    load._save_border(_name, _start)
    # clean directory
    output = load.model_grid_data_path / ("test" + ".geojson")
    output.unlink()

    all_entries = ModelGrid.objects.all()

    # one element on database
    assert len(all_entries) == 1
    assert all_entries[0].name == "test"


def test__save_border_raises_no_exception(tmp_path):
    """
    GIVEN a name associated to a valid geojson file
    WHEN  running _save
    THEN  raise no Exception
    """
    # create dummy netcdf file
    thredd = "https://thredds.met.no/thredds/dodsC/metpplatest/met_forecast_1_0km_nordic_latest.nc"
    _name = "test"
    _start = dt.datetime.fromtimestamp(0).isoformat()
    _end = _start

    ds = nc.Dataset(thredd, "r")

    load._setup_border(ds, _name, _start, _end)
    try:
        load._save_border(_name, _start)
    except Exception as exc:
        assert False, f"'load._save_border()' raised an exception {exc}"

    # clean directory
    output = load.model_grid_data_path / ("test" + ".geojson")
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


def test__check_param_data_date_valid():
    """
    GIVEN a dictionary
     with 'data' key's value which is a dictionary
     with a model_name value which is a dictionary
     with an 'url' key with a valid thredd path or file
     and
     with an 'date_valid_start' key with a invalid datetime
    WHEN  checking it
    THEN  raise TypeError
     with error message starting with "Invalid datetime format"
     and ending with "\nCheck whatever"
    """
    thredd = "https://thredds.met.no/thredds/dodsC/metpplatest/met_forecast_1_0km_nordic_latest.nc"
    dict = {"data": {"model_name": {"url": thredd, "date_valid_start": "2020-13-01"}}}
    with pytest.raises(ValueError) as execinfo:
        load._check_param(dict, "whatever")
    # check error message
    assert str(execinfo.value).startswith("Invalid datetime format")
    assert str(execinfo.value).endswith("\nCheck whatever")

    dict = {"data": {"model_name": {"url": thredd, "date_valid_start": ""}}}
    with pytest.raises(ValueError) as execinfo:
        load._check_param(dict, "whatever")
    # check error message
    assert str(execinfo.value).startswith("Invalid datetime format")
    assert str(execinfo.value).endswith("\nCheck whatever")

    dict = {"data": {"model_name": {"url": thredd, "date_valid_start": None}}}
    with pytest.raises(ValueError) as execinfo:
        load._check_param(dict, "whatever")
    # check error message
    assert str(execinfo.value).startswith("Invalid datetime format")
    assert str(execinfo.value).endswith("\nCheck whatever")


def test__check_param_data_url():
    """
    GIVEN a dictionary
     with 'data' key's value which is a dictionary
     with a model_name value which is a dictionary
     with an 'url' key with a invalid thredd path or file
     and
     with an 'date_valid_start' key with a valid datetime
    WHEN  checking it
    THEN  raise TypeError
     with error message starting with "Invalid URL for model grid"
     and ending with "must be an url or an existing file.\nCheck whatever"
    """
    thredd = "thredds/dodsC/metpplatest/met_forecast_1_0km_nordic_latest.nc"
    dict = {"data": {"model_name": {"url": thredd, "date_valid_start": "2020-01-01"}}}
    with pytest.raises(ValueError) as execinfo:
        load._check_param(dict, "whatever")
    # check error message
    assert str(execinfo.value).startswith("Invalid URL for model grid")
    assert str(execinfo.value).endswith(
        "must be an url or an existing file.\nCheck whatever"
    )


def test__check_param_raises_no_exception():
    """
    GIVEN a dictionary
     with 'data' key's value which is a dictionary
     with a model_name value which is a dictionary
     with an 'url' key with a valid thredd path or file
     and
     with an 'date_valid_start' key with a valid datetime
    WHEN  checking it
    THEN  raise no Exception
    """
    thredd = "https://thredds.met.no/thredds/dodsC/metpplatest/met_forecast_1_0km_nordic_latest.nc"
    dict = {"data": {"model_name": {"url": thredd, "date_valid_start": "2020-01-01"}}}
    try:
        load._check_param(dict, "whatever")
    except Exception as exc:
        assert False, f"'load._check_param()' raised an exception {exc}"


def test_upload_yaml(tmp_path):
    """
    GIVEN an invalid yaml input file
    WHEN  running up
    THEN  raise Exception
     with error message starting with 'Something goes wrong when uploading extra parameters file'
    """
    _tmp = None
    with pytest.raises(Exception) as execinfo:
        load.up(_tmp)

    # check error message
    assert str(execinfo.value).startswith(
        "Something goes wrong when uploading extra parameters"
    )

    dict = {"data": "something"}
    _tmp = tmp_path / "meta.yaml"
    with open(_tmp, "w+") as ff:
        yaml.dump(dict, ff, allow_unicode=True, default_flow_style=False)

    with pytest.raises(Exception) as execinfo:
        load.run(_tmp)


def test_upload_raises_no_exception():
    """
    GIVEN an valid yaml input file
    WHEN  running up
    THEN  raise no Exception
    """
    """
    Assert your python code raises no exception.
    """
    try:
        load.up()
    except Exception as exc:
        assert False, f"'load.run()' raised an exception {exc}"


@pytest.mark.skip(reason="useless ??")
def test_upload_yaml_success():
    """
    GIVEN an valid yaml input file
    WHEN  running up
    THEN  'geojosn' file(s) created on load.model_grid_data_path
     and  element(s) added to the database
    """
    load.up()
    fparam_ = load.model_grid_path / "data.yaml"
    with open(fparam_, "r") as stream:
        try:
            param = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    # check geojson exist
    for f in param["data"].keys():
        output = load.model_grid_data_path / (f + ".geojson")
        assert output.exists()
        assert output.is_file()
    # check instance on database
    all_entries = ModelGrid.objects.all()

    # all elements on database
    assert len(all_entries) == len(param["data"])
