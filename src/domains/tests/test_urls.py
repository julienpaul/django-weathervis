# Stdlib imports
import pytest

# Core Django imports
from django.urls import resolve, reverse

# Third-party app imports
# Imports from my apps
from src.domains.models import Domain

pytestmark = pytest.mark.django_db


class TestDomainView:
    def test_list(self):
        assert reverse("domains:list") == "/domains/"
        assert resolve("/domains/").view_name == "domains:list"

    def test_add(self):
        assert reverse("domains:create") == "/domains/~add/"
        assert resolve("/domains/~add/").view_name == "domains:create"

    def test_detail(self, domain: Domain):
        assert (
            reverse("domains:detail", kwargs={"slug": domain.slug})
            == f"/domains/{domain.slug}/"
        )
        assert resolve(f"/domains/{domain.slug}/").view_name == "domains:detail"

    def test_update(self, domain: Domain):
        assert (
            reverse("domains:update", kwargs={"slug": domain.slug})
            == f"/domains/{domain.slug}/~update/"
        )
        assert resolve(f"/domains/{domain.slug}/~update/").view_name == "domains:update"

    def test_delete(self, domain: Domain):
        assert (
            reverse("domains:delete", kwargs={"slug": domain.slug})
            == f"/domains/~delete/{domain.slug}/"
        )
        assert resolve(f"/domains/~delete/{domain.slug}/").view_name == "domains:delete"
