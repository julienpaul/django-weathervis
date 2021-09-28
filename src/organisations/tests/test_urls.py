# Stdlib imports
import pytest

# Core Django imports
from django.urls import resolve, reverse

# Third-party app imports
# Imports from my apps
from src.organisations.models import Organisation

pytestmark = pytest.mark.django_db


def test_list():
    assert reverse("organisations:list") == "/organisations/"
    assert resolve("/organisations/").view_name == "organisations:list"


def test_delete(organisation: Organisation):
    assert (
        reverse("organisations:delete", kwargs={"pk": organisation.id})
        == f"/organisations/~delete/{organisation.id}/"
    )
    assert (
        resolve(f"/organisations/~delete/{organisation.id}/").view_name
        == "organisations:delete"
    )
