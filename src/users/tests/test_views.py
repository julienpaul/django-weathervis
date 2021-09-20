# Stdlib imports
import pytest

# Core Django imports
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import AnonymousUser
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.http import HttpRequest
from django.test import RequestFactory
from django.urls import reverse

# Third-party app imports
from pytest_django.asserts import assertContains, assertTemplateUsed

# Imports from my apps
from src.users.forms import UserUpdateForm
from src.users.models import User
from src.users.tests.factories import UserFactory
from src.users.views import (
    UserRedirectView,
    UserUpdateView,
    user_detail_view,
    user_update_view,
)

pytestmark = pytest.mark.django_db


class TestUserUpdateView:
    """
    TODO:
        extracting view initialization code as class-scoped fixture
        would be great if only pytest-django supported non-function-scoped
        fixture db access -- this is a work-in-progress for now:
        https://github.com/pytest-dev/pytest-django/pull/258
    """

    def dummy_get_response(self, request: HttpRequest):
        return None

    def test_get_success_url(self, user: User, rf: RequestFactory):
        view = UserUpdateView()
        request = rf.get("/fake-url/")
        request.user = user

        view.request = request

        assert view.get_success_url() == f"/users/@{user.username}/"

    def test_get_object(self, user: User, rf: RequestFactory):
        view = UserUpdateView()
        request = rf.get("/fake-url/")
        request.user = user

        view.request = request

        assert view.get_object() == user

    def test_form_valid(self, user: User, rf: RequestFactory):
        view = UserUpdateView()
        request = rf.get("/fake-url/")

        # Add the session/message middleware to the request
        SessionMiddleware(self.dummy_get_response).process_request(request)
        MessageMiddleware(self.dummy_get_response).process_request(request)
        request.user = user

        view.request = request

        # Initialize the form
        form = UserUpdateForm()
        form.cleaned_data = []
        view.form_valid(form)

        messages_sent = [m.message for m in messages.get_messages(request)]
        assert messages_sent == ["Information successfully updated"]

    def test_contains_form(self, user: User, client):
        url = reverse("users:update")
        client.force_login(user)
        response = client.get(url)

        form = response.context.get("form")

        assert isinstance(form, UserUpdateForm)

    def test_form_buttons(self, user: User, client):
        """ """
        url = reverse("users:update")
        client.force_login(user)
        response = client.get(url)

        assertContains(response, 'input type="submit"', 1)
        assertContains(response, 'input type="button"', 1)

    def test_csrf(self, user: User, rf: RequestFactory):
        request = rf.get("/fake-url/")
        request.user = UserFactory()

        response = user_update_view(request)

        assertContains(response, "csrfmiddlewaretoken")

    def test_template(self, user: User, client):
        url = reverse("users:update")
        client.force_login(user)
        response = client.get(url)
        assertTemplateUsed(response, "users/user_form.html")

    def test_authenticated(self, user: User, rf: RequestFactory):
        request = rf.get("/fake-url/")
        request.user = UserFactory()

        response = user_update_view(request, username=user.username)

        assert response.status_code == 200

    def test_not_authenticated(self, user: User, rf: RequestFactory):
        request = rf.get("/fake-url/")
        request.user = AnonymousUser()

        response = user_update_view(request, username=user.username)
        login_url = reverse(settings.LOGIN_URL)

        assert response.status_code == 302
        assert response.url == f"{login_url}?next=/fake-url/"


class TestUserRedirectView:
    def test_get_redirect_url(self, user: User, rf: RequestFactory):
        view = UserRedirectView()
        request = rf.get("/fake-url")
        request.user = user

        view.request = request

        assert view.get_redirect_url() == f"/users/@{user.username}/"


class TestUserDetailView:
    def test_authenticated(self, user: User, rf: RequestFactory):
        request = rf.get("/fake-url/")
        request.user = UserFactory()

        response = user_detail_view(request, username=user.username)

        assert response.status_code == 200

    def test_not_authenticated(self, user: User, rf: RequestFactory):
        request = rf.get("/fake-url/")
        request.user = AnonymousUser()

        response = user_detail_view(request, username=user.username)
        login_url = reverse(settings.LOGIN_URL)

        assert response.status_code == 302
        assert response.url == f"{login_url}?next=/fake-url/"

    def test_template(self, user: User, client):
        url = reverse("users:detail", kwargs={"username": user.username})
        client.force_login(user)
        response = client.get(url)
        assertTemplateUsed(response, "users/user_detail.html")

    def test_contains_buttons(self, user: User, client):
        """
        GIVEN one user
        WHEN  accessing his own profil
        THEN  should see 2 buttons
        """
        url = reverse("users:detail", kwargs={"username": user.username})
        client.force_login(user)
        response = client.get(url)
        assertContains(response, 'role="button"', 2)

    def test_contains_no_buttons(self, user: User, user2: User, client):
        """
        GIVEN two users
        WHEN  one accesses the profile of the second
        THEN  he should not see any button
        """
        url = reverse("users:detail", kwargs={"username": user2.username})
        client.force_login(user)
        response = client.get(url)
        assertContains(response, 'role="button"', 0)
