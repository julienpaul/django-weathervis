# Stdlib import
import pytest

# Core Django imports
# Third-party app imports
# Imports from my apps
from src.weather_forecasts.models import WeatherForecastBorder

pytestmark = pytest.mark.django_db


def test__str__(weatherForecastBorder: WeatherForecastBorder):
    """
    GIVEN an WeatherForecastBorder instance
    WHEN  printing the instance (without any attributes)
    THEN  return the weatherForecastBorder name
    """
    assert str(weatherForecastBorder) == f"{weatherForecastBorder.name}"
