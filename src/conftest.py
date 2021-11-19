# Stdlib imports
import pytest

# Core Django imports
# Third-party app imports
# Imports from my app
from src.organisations.models import Organisation
from src.organisations.tests.factories import OrganisationFactory
from src.users.models import User
from src.users.tests.factories import UserFactory
from src.weather_forecasts.models import WeatherForecastBorder
from src.weather_forecasts.tests.factories import WeatherForecastBorderFactory


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user() -> User:
    return UserFactory()


@pytest.fixture
def user2() -> User:
    return UserFactory()


@pytest.fixture
def staff() -> User:
    return UserFactory(staff=True)


@pytest.fixture
def organisation() -> Organisation:
    return OrganisationFactory()


@pytest.fixture
def weatherForecastBorder() -> WeatherForecastBorder:
    return WeatherForecastBorderFactory()
