# Stdlib imports
import pytest

# Core Django imports
from django.urls import resolve, reverse

# Third-party app imports
# Imports from my apps
from src.stations.models import Station

pytestmark = pytest.mark.django_db


class TestStationView:
    def test_list(self):
        assert reverse("stations:list") == "/stations/~list/"
        assert resolve("/stations/~list/").view_name == "stations:list"

    def test_add(self):
        assert reverse("stations:create") == "/stations/~add/"
        assert resolve("/stations/~add/").view_name == "stations:create"

    def test_detail(self, station: Station):
        assert (
            reverse("stations:detail", kwargs={"slug": station.slug})
            == f"/stations/~detail/{station.slug}/"
        )
        assert (
            resolve(f"/~detail/stations/{station.slug}/").view_name == "stations:detail"
        )

    def test_update(self, station: Station):
        assert (
            reverse("stations:update", kwargs={"slug": station.slug})
            == f"/stations/~update/{station.slug}/"
        )
        assert (
            resolve(f"/stations/~update/{station.slug}/").view_name == "stations:update"
        )

    def test_delete(self, station: Station):
        assert (
            reverse("stations:delete", kwargs={"slug": station.slug})
            == f"/stations/~delete/{station.slug}/"
        )
        assert (
            resolve(f"/stations/~delete/{station.slug}/").view_name == "stations:delete"
        )
