# Stdlib imports
import pytest

# Core Django imports
from django.urls import resolve, reverse

# Third-party app imports
# Imports from my apps
from src.margins.models import Margin

pytestmark = pytest.mark.django_db


class TestMarginView:
    def test_list(self):
        assert reverse("margins:list") == "/margins/"
        assert resolve("/margins/").view_name == "margins:list"

    def test_delete(self, margin: Margin):
        assert (
            reverse("margins:delete", kwargs={"pk": margin.pk})
            == f"/margins/~delete/{margin.pk}/"
        )
        assert resolve(f"/margins/~delete/{margin.pk}/").view_name == "margins:delete"
