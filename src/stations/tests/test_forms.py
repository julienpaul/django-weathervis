# Stdlib imports
import pytest

# Core Django imports
from django.utils.translation import gettext_lazy as _

# Third-party app imports
# Imports from my apps
from src.stations.forms import StationForm
from src.stations.models import Station
from src.utils import util
from src.weather_forecasts.models import WeatherForecastBorder


@pytest.mark.django_db
class TestStationForm:
    """
    Test class for all tests related to the StationForm
    """

    def test_init_helper_layout(self):
        """
        GIVEN class StationForm
        WHEN  initialised an instance
        THEN  instance should have attribute 'helper' and 'helper.layout'
        """
        form = StationForm()
        assert hasattr(form, "helper")
        assert hasattr(form.helper, "layout")

    @pytest.mark.skip(reason="test not implemented yet")
    def test_longitude(self, station: Station):
        """ "
        GIVEN an invalid longitude
        WHEN  initiate stationForm
        THEN  raises en Error
        """
        # # min_value=-180,
        # data["lon"] = -200
        # # max_value=180,
        # data["lon"] = 200
        # # max_digits=9,
        # data["lon"] = 1200.123456
        # # decimal_places=6,
        # data["lon"] = 0.1234567

    def test_clean_raises_validation_error(
        self, station: Station, weatherForecastBorder: WeatherForecastBorder
    ):
        """
        GIVEN a StationForm instance
        WHEN  station located outside WeatherForecastBorder
        THEN  raises a ValidationError
         with an error message "Station is not inside any WeatherForecastBorder registered."
        """

        centroid = weatherForecastBorder.geom.centroid
        # define point on the other side of the earth
        antipode = util.antipode(centroid)
        _lon = round(antipode.x, 6)
        _lat = round(antipode.y, 6)
        _alt = round(station.altitude, 6)

        data = {
            "name": "another station",
            "longitude": _lon,
            "latitude": _lat,
            "altitude": _alt,
            "station_id": "something 999",
            "wmo_id": "any99",
            "description": "blablabla",
            "margin": station.margin,
        }
        form = StationForm(data)

        assert not form.is_valid()
        # DecimalField max_digits counts negative sign as a digit ???
        print(f"data {data}")
        assert len(form.errors) == 1
        assert "__all__" in form.errors
        assert form.errors["__all__"][0] == _(
            "Station is not inside any WeatherForecastBorder registered."
        )

    def test_clean_success(
        self, station: Station, weatherForecastBorder: WeatherForecastBorder
    ):
        """
        GIVEN a StationForm instance
        WHEN  adding a station located inside WeatherForecastBorder
        THEN  form is valid
        """

        centroid = weatherForecastBorder.geom.centroid  # centroïde de ce polygone
        _name = "another station"
        _lon = round(centroid.x, 6)
        _lat = round(centroid.y, 6)
        _alt = round(0, 6)

        data = {
            "name": _name,
            "longitude": _lon,
            "latitude": _lat,
            "altitude": _alt,
            "station_id": "someID_999",
            "wmo_id": "any99",
            "description": "blablabla",
            "margin": station.margin,
        }
        form = StationForm(data)

        assert form.is_valid()

    def test_form_is_valid_raises_no_exception(
        self, station: Station, weatherForecastBorder: WeatherForecastBorder
    ):
        """
        GIVEN a StationForm instance
        WHEN  adding a station located inside WeatherForecastBorder
        THEN  raise no Exception
        """
        centroid = weatherForecastBorder.geom.centroid  # centroïde de ce polygone
        _name = "another station"
        _lon = round(centroid.x, 6)
        _lat = round(centroid.y, 6)
        _alt = round(0, 6)

        data = {
            "name": _name,
            "longitude": _lon,
            "latitude": _lat,
            "altitude": _alt,
            "station_id": "someID_999",
            "wmo_id": "any99",
            "description": "blablabla",
            "margin": station.margin,
        }
        form = StationForm(data)

        try:
            form.is_valid()
        except Exception as exc:
            assert False, f"'form.is_valid()' raised an exception {exc}"
