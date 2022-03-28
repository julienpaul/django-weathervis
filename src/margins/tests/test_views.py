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
from src.margins.forms import MarginForm
from src.margins.models import Margin
from src.margins.views import (
    MarginCreateView,
    MarginDeleteView,
    MarginView,
    margin_view,
)
from src.users.models import User


@pytest.mark.django_db
class TestOrganisationView:
    def dummy_get_response(self, request: HttpRequest):
        return None

    def test_get_authenticated(self, rf: RequestFactory, user: User):
        request = rf.get("/fake-url/")
        request.user = user

        response = margin_view(request)
        assert response.status_code == 200

        # Use this syntax for class-based views.
        response = MarginView.as_view()(request)
        assert response.status_code == 200

    def test_get_not_authenticated(self, rf: RequestFactory):
        request = rf.get("/fake-url/")
        request.user = AnonymousUser()

        response = margin_view(request)
        login_url = reverse(settings.LOGIN_URL)

        assert response.status_code == 302
        assert response.url == f"{login_url}?next=/fake-url/"

    def test_get_template(self, client, user: User):
        url = reverse("margins:list")
        client.force_login(user)
        response = client.get(url)
        assertTemplateUsed(response, "margins/margin_list.html")

    def test_post_authenticated(self, rf: RequestFactory, user: User):
        request = rf.post("/fake-url/")
        # Add the session/message middleware to the request
        SessionMiddleware(self.dummy_get_response).process_request(request)
        MessageMiddleware(self.dummy_get_response).process_request(request)
        request.user = user

        response = margin_view(request)

        assert response.status_code == 200

    def test_post_not_authenticated(self, rf: RequestFactory):
        request = rf.post("/fake-url/")
        request.user = AnonymousUser()

        response = margin_view(request)
        login_url = reverse(settings.LOGIN_URL)

        assert response.status_code == 302
        assert response.url == f"{login_url}?next=/fake-url/"

    def test_post_template(self, client, user: User):
        url = reverse("margins:list")
        client.force_login(user)
        response = client.post(url)
        assertTemplateUsed(response, "margins/margin_list.html")


@pytest.mark.django_db
class TestMarginListView:
    def test_template(self, client, user: User):
        url = reverse("margins:list")
        client.force_login(user)
        response = client.get(url)
        assertTemplateUsed(response, "margins/margin_list.html")

    def test_context_data(self, rf: RequestFactory, user: User):
        """
        GIVEN a GET request of an instance of MarginView, and a user
        WHEN  displaying the list view
        THEN  context dictionnary should contain key 'margins' and 'form'
        """
        request = rf.get("/fake-url/")
        request.user = user

        response = margin_view(request)
        assert response.status_code == 200

        assert isinstance(response.context_data, dict)
        assert "margins" in response.context_data
        assert "form" in response.context_data
        assert isinstance(response.context_data["form"], MarginForm)

    @pytest.mark.skip(reason="test not implemented yet")
    def test_delete_button(self, client, staff: User, margin: Margin):
        """
        GIVEN one margin, and a staff member
        WHEN  display the list view
        THEN  one delete button should be display
        """
        url = reverse("margins:list")
        client.force_login(staff)
        response = client.get(url)

        assertContains(response, f'href="/margins/~delete/{margin.id}/"', 1)
        assertContains(response, 'class="btn btn-danger"', 1)

    @pytest.mark.skip(reason="test not implemented yet")
    def test_no_delete_button(self, client, user: User, margin: Margin):
        """
        GIVEN one margin,
          and a user (not in staff)
        WHEN  display the list view
        THEN  no delete button should be display
        """
        url = reverse("margins:list")
        client.force_login(user)
        response = client.get(url)

        assertContains(response, f'href="/margins/~delete/{margin.id}/"', 0)
        assertContains(response, 'class="btn btn-danger"', 0)

    @pytest.mark.skip(reason="test not implemented yet")
    def test_pagination(self):
        """
        GIVEN N organistions
        WHEN  display the list view
        THEN  should see X pages
        """
        pass


class TestSuccessURLAllowedHostsMixin:
    @pytest.mark.skip(reason="test not implemented yet")
    def test_get_success_url_allowed_hosts(self):
        pass


@pytest.mark.django_db
class TestMarginCreateView:
    def dummy_get_response(self, request: HttpRequest):
        return None

    def test_template(self, client, user: User):
        url = reverse("margins:list")
        client.force_login(user)
        response = client.post(url)
        assertTemplateUsed(response, "margins/margin_list.html")

    def test_context_data(self, rf: RequestFactory, user: User):
        """
        GIVEN a POST request of an instance of MarginView,
          and a user
        WHEN  displaying the list view
        THEN  context dictionnary should contain key 'margins' and 'form'
        """
        request = rf.post("/fake-url/")
        # Add the session/message middleware to the request
        SessionMiddleware(self.dummy_get_response).process_request(request)
        MessageMiddleware(self.dummy_get_response).process_request(request)
        request.user = user

        response = margin_view(request)
        assert response.status_code == 200

        assert isinstance(response.context_data, dict)
        assert "form" in response.context_data
        assert isinstance(response.context_data["form"], MarginForm)

    def test_context_form(self, client, user: User, margin: Margin):
        url = reverse("margins:list")
        client.force_login(user)
        response = client.get(url)

        form = response.context.get("form")

        assert isinstance(form, MarginForm)

    def test_csrf(self, rf: RequestFactory, user: User):
        request = rf.get("/fake-url/")
        request.user = user

        response = margin_view(request)

        assertContains(response, "csrfmiddlewaretoken")

    def test_form_buttons(self, client, user: User):
        """ """
        url = reverse("margins:list")
        client.force_login(user)
        response = client.get(url)

        assertContains(response, 'input type="submit"', 1)

    def test_form_valid(self, rf: RequestFactory, user: User):
        """
        GIVEN an instance of MarginCreateView
          and a user
        WHEN  posting an valid MarginForm
        THEN  the form should be valid
          and a success message should appear
        """
        view = MarginCreateView()
        request = rf.get("/fake-url/")

        # Add the session/message middleware to the request
        SessionMiddleware(self.dummy_get_response).process_request(request)
        MessageMiddleware(self.dummy_get_response).process_request(request)
        request.user = user

        # view.request = request
        view.setup(request)

        # Initialize the form
        data = {
            "east": 0,
            "west": 0,
            "north": 0,
            "south": 0,
        }
        form = MarginForm(data)
        form.cleaned_data = []
        assert form.is_valid()
        view.form_valid(form)

        messages_sent = [m.message for m in messages.get_messages(request)]
        assert messages_sent == ["Margin successfully added"]

    @pytest.mark.skip(reason="test not implemented yet")
    def test_form_invalid(self, rf: RequestFactory, user: User, margin: Margin):
        """
        GIVEN an instance of MarginCreateView
          and a user
        WHEN  posting an invalid MarginForm
        THEN  the form should be invalid
          and an error message should appear
        """
        view = MarginCreateView()
        request = rf.get("/fake-url/")

        # Add the session/message middleware to the request
        SessionMiddleware(self.dummy_get_response).process_request(request)
        MessageMiddleware(self.dummy_get_response).process_request(request)
        request.user = user

        view.setup(request)

        # Initialize the form
        data = {
            "east": margin.east,
            "west": margin.west,
            "north": margin.north,
            "south": margin.south,
        }
        form = MarginForm(data)
        form.cleaned_data = []
        assert not form.is_valid()

        view.form_invalid(form)

        messages_sent = [m.message for m in messages.get_messages(request)]
        assert messages_sent == [
            "Margin with this West, East, North and South already exists."
        ]

    @pytest.mark.skip(reason="test not implemented yet")
    def test_get_next_page(self, rf: RequestFactory, user: User):
        """
        GIVEN an instance of MarginCreateView,
          and a user
        WHEN
        THEN

        1. no redirect_field_name in self.request.POST or GET
        1.1 next_page == None
        1.2 next_page != None
        2. redirect_field_name in self.request.POST or GET
        2.1 get next from url
        2.2 url_is_safe using url_has_allowed_host_and_scheme (mixin)
        2.3 url_is_not_safe redirect to self.request.path
        """
        pass

    @pytest.mark.skip(reason="test not implemented yet")
    def test_success_url(self, rf: RequestFactory, user: User):
        """
        GIVEN an instance of MarginCreateView,
          and a user
        WHEN
        THEN  should redirect to the margins list url

        1. next_page from get_next_page is None
        1.1 run super().get_success_url()
        """
        view = MarginCreateView()
        request = rf.get("/fake-url/")
        request.user = user

        form = MarginForm()
        form.cleaned_data = []

        view.setup(request)
        view.next_page = None
        url = view.get_success_url()
        success_url = reverse("margins:list")

        assert url == success_url


@pytest.mark.django_db
class TestMarginDeleteView:
    def dummy_get_response(self, request: HttpRequest):
        return None

    def test_template(self, client, staff: User, margin: Margin):
        """
        GIVEN an instance of MarginDeleteView,
          and a staff member
        WHEN  requesting the deletion of an margin
        THEN  should return the confirm_delete template
        """
        url = reverse("margins:delete", kwargs={"pk": margin.id})
        client.force_login(staff)
        response = client.get(url)
        assertTemplateUsed(response, "margins/margin_confirm_delete.html")

    def test_success_message(self, rf: RequestFactory, staff: User, margin: Margin):
        """
        GIVEN an instance of MarginDeleteView,
          and a staff member
        WHEN  deleting successfuly the margin
        THEN  should return a success message
        """
        request = rf.delete("/fake-url/")

        # Add the session/message middleware to the request
        SessionMiddleware(self.dummy_get_response).process_request(request)
        MessageMiddleware(self.dummy_get_response).process_request(request)
        request.user = staff

        MarginDeleteView.as_view()(request, pk=margin.id)

        messages_sent = [m.message for m in messages.get_messages(request)]
        assert messages_sent == ["Margin successfully removed"]

    def test_delete_from_db(self, client, staff: User, margin: Margin):
        """
        GIVEN an instance of _MarginDeleteView,
          and a staff member
        WHEN  deleting successfuly the margin
        THEN  databse should not contain any margin
        """
        url = reverse("margins:delete", kwargs={"pk": margin.id})
        client.force_login(staff)
        client.delete(url)

        assert Margin.objects.count() == 0

    def test_redirect_client(self, client, staff: User, margin: Margin):
        """
        GIVEN an instance of MarginDeleteView,
          and a staff member
        WHEN  deleting successfuly the margin
        THEN  should be redirect to margins list page,
         with  status code 302
        """
        url = reverse("margins:delete", kwargs={"pk": margin.id})
        client.force_login(staff)
        response = client.delete(url, follow=True)
        success_url = reverse("margins:list")

        redirect_url = response.redirect_chain[-1][0]
        redirect_status_code = response.redirect_chain[-1][1]
        assert redirect_url == f"{success_url}"
        assert redirect_status_code == 302

    def test_redirect(self, rf: RequestFactory, staff: User, margin: Margin):
        """
        GIVEN an instance of MarginDeleteView,
          and a staff member
          and a margin
        WHEN  deleting successfuly the margin
        THEN  should be redirect to margins list page,
         with  status code 302
        """
        request = rf.delete("/fake-url/")
        request.user = staff
        # Add the session/message middleware to the request
        SessionMiddleware(self.dummy_get_response).process_request(request)
        MessageMiddleware(self.dummy_get_response).process_request(request)

        response = MarginDeleteView.as_view()(request, pk=margin.id)
        success_url = reverse("margins:list")

        assert response.status_code == 302
        assert response.url == f"{success_url}"

    @pytest.mark.skip(reason="test not implemented yet")
    def test_redirect_error(self, rf: RequestFactory, user: User):
        """
        GIVEN
        WHEN
        THEN
        """
        pass

    def test_get_not_authenticated(self, rf: RequestFactory, user: User):
        request = rf.get("/fake-url/")
        request.user = AnonymousUser()

        response = margin_view(request)
        login_url = reverse(settings.LOGIN_URL)

        assert response.status_code == 302
        assert response.url == f"{login_url}?next=/fake-url/"

    @pytest.mark.skip(reason="test not implemented yet")
    def test_user_permission(self, rf: RequestFactory, user: User):
        """
        GIVEN
        WHEN
        THEN
        a no staff member should not be able to delete organisation
        """
        pass
