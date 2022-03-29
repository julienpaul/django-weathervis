# Stdlib imports
import pytest

# Core Django imports
from django.urls import resolve, reverse

# Third-party app imports
# Imports from my apps
from src.users.models import User

pytestmark = pytest.mark.django_db


class TestUserView:
    def test_detail(self, user: User):
        assert (
            reverse("users:detail", kwargs={"username": user.username})
            == f"/users/@{user.username}/"
        )
        assert resolve(f"/users/@{user.username}/").view_name == "users:detail"

    def test_update(self):
        assert reverse("users:update") == "/users/~update/"
        assert resolve("/users/~update/").view_name == "users:update"

    def test_redirect(self):
        assert reverse("users:redirect") == "/users/~redirect/"
        assert resolve("/users/~redirect/").view_name == "users:redirect"

    def test_upgrade_request(self):
        assert reverse("users:upgrade_request") == "/users/~upgrade/request/"
        assert resolve("/users/~upgrade/request/").view_name == "users:upgrade_request"
