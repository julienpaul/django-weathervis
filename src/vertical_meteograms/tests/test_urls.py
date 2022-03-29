# Stdlib imports
import pytest

# Core Django imports
from django.urls import resolve, reverse

# Third-party app imports
# Imports from my apps
from src.vertical_meteograms.models import VerticalMeteogram

pytestmark = pytest.mark.django_db


class TestVerticalMeteogramView:
    def test_redirect(self):
        assert reverse("vmeteograms:redirect") == "/vmeteograms/"
        assert resolve("/vmeteograms/").view_name == "vmeteograms:redirect"

    def test_list(self):
        assert reverse("vmeteograms:list") == "/vmeteograms/list/"
        assert resolve("/vmeteograms/list/").view_name == "vmeteograms:list"

    def test_add(self):
        assert reverse("vmeteograms:create") == "/vmeteograms/~add/"
        assert resolve("/vmeteograms/~add/").view_name == "vmeteograms:create"

    def test_detail(self, vmeteogram: VerticalMeteogram):
        assert (
            reverse("vmeteograms:detail", kwargs={"slug": vmeteogram.slug})
            == f"/vmeteograms/{vmeteogram.slug}/"
        )
        assert (
            resolve(f"/vmeteograms/{vmeteogram.slug}/").view_name
            == "vmeteograms:detail"
        )

    def test_change_plot(self):
        assert reverse("vmeteograms:change_plot") == "/vmeteograms/ajax/change_plot/"
        assert (
            resolve("/vmeteograms/ajax/change_plot/").view_name
            == "vmeteograms:change_plot"
        )

    def test_show_plot(self):
        assert reverse("vmeteograms:show_plot") == "/vmeteograms/ajax/show_plot/"
        assert (
            resolve("/vmeteograms/ajax/show_plot/").view_name == "vmeteograms:show_plot"
        )
