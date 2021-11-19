# Stdlib imports
import pytest

# Core Django imports
# Third-party app imports
from faker import Faker

# Imports from my app
from src.margins.models import Margin
from src.margins.tests.factories import MarginFactory
from src.organisations.models import Organisation
from src.organisations.tests.factories import OrganisationFactory
from src.stations.models import Station
from src.stations.tests.factories import StationFactory
from src.users.models import User
from src.users.tests.factories import UserFactory
from src.utils.tests.factories import DjangoGeoPointProvider
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


@pytest.fixture
def geopoint():
    fake = Faker()
    fake.add_provider(DjangoGeoPointProvider)
    point = fake.geo_point()
    return point


@pytest.fixture
def station() -> Station:
    return StationFactory()


@pytest.fixture
def margin() -> Margin:
    return MarginFactory()
