# Stdlib imports
import pytest

# Core Django imports
from django.core.management import call_command

# Third-party app imports
from faker import Faker

# Imports from my app
from src.margins.models import Margin
from src.margins.tests.factories import MarginFactory
from src.model_grids.models import ModelGrid
from src.model_grids.tests.factories import ModelGridFactory
from src.organisations.models import Organisation
from src.organisations.tests.factories import OrganisationFactory
from src.stations.models import Station
from src.stations.tests.factories import StationFactory
from src.surface_meteograms.models import SurfaceMeteogram
from src.surface_meteograms.tests.factories import SurfaceMeteogramFactory
from src.users.models import User
from src.users.tests.factories import UserFactory, get_group, get_permission
from src.utils.tests.factories import DjangoGeoPointProvider
from src.vertical_meteograms.models import VerticalMeteogram
from src.vertical_meteograms.tests.factories import VerticalMeteogramFactory


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command("create_groups")


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture()
def user(request) -> User:
    user = UserFactory()
    if hasattr(request, "param"):
        if "groups" in request.param:
            list_groups = request.param["groups"]
            if not isinstance(list_groups, list):
                list_groups = [list_groups]
            for group in list_groups:
                user.groups.add(get_group(group))
        if "permissions" in request.param:
            list_perms = request.param["permissions"]
            if not isinstance(list_perms, list):
                list_perms = [list_perms]
            for perm in list_perms:
                user.permissions.add(get_permission(perm))
    return user


@pytest.fixture()
def user2(request) -> User:
    user = UserFactory()
    if hasattr(request, "param"):
        if "groups" in request.param:
            list_groups = request.param["groups"]
            if not isinstance(list_groups, list):
                list_groups = [list_groups]
            for group in list_groups:
                user.groups.add(get_group(group))
        if "permissions" in request.param:
            list_perms = request.param["permissions"]
            if not isinstance(list_perms, list):
                list_perms = [list_perms]
            for perm in list_perms:
                user.permissions.add(get_permission(perm))
    return user


@pytest.fixture
def staff() -> User:
    staff = UserFactory(staff=True)
    staff.groups.add(get_group("Staff"))
    return staff


@pytest.fixture
def organisation() -> Organisation:
    return OrganisationFactory()


@pytest.fixture
def modelGrid() -> ModelGrid:
    return ModelGridFactory()


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


@pytest.fixture
def smeteogram() -> SurfaceMeteogram:
    return SurfaceMeteogramFactory()


@pytest.fixture
def vmeteogram() -> VerticalMeteogram:
    return VerticalMeteogramFactory()
