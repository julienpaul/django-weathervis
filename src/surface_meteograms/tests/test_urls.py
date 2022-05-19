# Stdlib imports
import pytest

# Core Django imports
from django.urls import resolve, reverse

# Third-party app imports
# Imports from my apps
from src.surface_meteograms.models import SurfaceMeteogram

pytestmark = pytest.mark.django_db


class TestSurfaceMeteogramView:
    def test_redirect(self):
        assert reverse("smeteograms:redirect") == "/smeteograms/"
        assert resolve("/smeteograms/").view_name == "smeteograms:redirect"

    def test_list(self):
        assert reverse("smeteograms:list") == "/smeteograms/list/"
        assert resolve("/smeteograms/list/").view_name == "smeteograms:list"

    def test_add(self):
        assert reverse("smeteograms:create") == "/smeteograms/~add/"
        assert resolve("/smeteograms/~add/").view_name == "smeteograms:create"

    def test_detail(self, smeteogram: SurfaceMeteogram):
        assert (
            reverse("smeteograms:detail", kwargs={"slug": smeteogram.slug})
            == f"/smeteograms/{smeteogram.slug}/"
        )
        assert (
            resolve(f"/smeteograms/{smeteogram.slug}/").view_name
            == "smeteograms:detail"
        )

    def test_change_plot(self):
        assert (
            reverse("smeteograms:change_plot") == "/smeteograms/ajax/data_change_plot/"
        )
        assert (
            resolve("/smeteograms/ajax/data_change_plot/").view_name
            == "smeteograms:change_plot"
        )

    def test_show_plot(self):
        assert reverse("smeteograms:show_plot") == "/smeteograms/ajax/data_show_plot/"
        assert (
            resolve("/smeteograms/ajax/data_show_plot/").view_name
            == "smeteograms:show_plot"
        )
