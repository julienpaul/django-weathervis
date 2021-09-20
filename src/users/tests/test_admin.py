# Stdlib imports
import pytest

# Core Django imports
from django.urls import reverse

# Third-party app imports
# Imports from my apps
from src.users.models import User

pytestmark = pytest.mark.django_db


class TestUserAdmin:
    def test_changelist(self, admin_client):
        """
        GIVEN an admin user
        WHEN  connecting to the changelist page
        THEN  status should be 200
        """
        url = reverse("admin:users_user_changelist")
        response = admin_client.get(url)
        assert response.status_code == 200

    def test_search(self, admin_client):
        """
        GIVEN an admin user
        WHEN
        THEN status should be 200
        """
        url = reverse("admin:users_user_changelist")
        response = admin_client.get(url, data={"q": "test"})
        assert response.status_code == 200

    def test_add(self, admin_client):
        """
        GIVEN an admin user
        WHEN  connecting to the add page
         and  adding a new user
        THEN  status should be 200
         and  new user should have been added
        """
        url = reverse("admin:users_user_add")
        response = admin_client.get(url)
        assert response.status_code == 200

        response = admin_client.post(
            url,
            data={
                "username": "test",
                "password1": "My_R@ndom-P@ssw0rd",
                "password2": "My_R@ndom-P@ssw0rd",
            },
        )
        assert response.status_code == 302
        assert User.objects.filter(username="test").exists()

    def test_view_user(self, admin_client):
        """
        GIVEN an admin user
        WHEN
        THEN
        """
        user = User.objects.get(username="admin")
        url = reverse("admin:users_user_change", kwargs={"object_id": user.pk})
        response = admin_client.get(url)
        assert response.status_code == 200
