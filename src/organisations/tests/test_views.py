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

from src.organisations.forms import OrganisationForm
from src.organisations.models import Organisation
from src.organisations.views import (
    OrganisationCreateView,
    OrganisationDeleteView,
    OrganisationView,
    organisation_view,
)

# Imports from my apps
from src.users.models import User


@pytest.mark.django_db
class TestOrganisationView:
    def dummy_get_response(self, request: HttpRequest):
        return None

    def test_get_authenticated(self, user: User, rf: RequestFactory):
        request = rf.get("/fake-url/")
        request.user = user

        response = organisation_view(request)
        assert response.status_code == 200

        # Use this syntax for class-based views.
        response = OrganisationView.as_view()(request)
        assert response.status_code == 200

    def test_get_not_authenticated(self, user: User, rf: RequestFactory):
        request = rf.get("/fake-url/")
        request.user = AnonymousUser()

        response = organisation_view(request)
        login_url = reverse(settings.LOGIN_URL)

        assert response.status_code == 302
        assert response.url == f"{login_url}?next=/fake-url/"

    def test_get_template(self, user: User, client):
        url = reverse("organisations:list")
        client.force_login(user)
        response = client.get(url)
        assertTemplateUsed(response, "organisations/organisation_list.html")

    def test_post_authenticated(self, user: User, rf: RequestFactory):
        request = rf.post("/fake-url/")
        # Add the session/message middleware to the request
        SessionMiddleware(self.dummy_get_response).process_request(request)
        MessageMiddleware(self.dummy_get_response).process_request(request)
        request.user = user

        response = organisation_view(request)

        assert response.status_code == 200

    def test_post_not_authenticated(self, user: User, rf: RequestFactory):
        request = rf.post("/fake-url/")
        request.user = AnonymousUser()

        response = organisation_view(request)
        login_url = reverse(settings.LOGIN_URL)

        assert response.status_code == 302
        assert response.url == f"{login_url}?next=/fake-url/"

    def test_post_template(self, user: User, client):
        url = reverse("organisations:list")
        client.force_login(user)
        response = client.post(url)
        assertTemplateUsed(response, "organisations/organisation_list.html")


@pytest.mark.django_db
class TestOrganisationListView:
    def test_template(self, user: User, client):
        url = reverse("organisations:list")
        client.force_login(user)
        response = client.get(url)
        assertTemplateUsed(response, "organisations/organisation_list.html")

    def test_context_data(self, user: User, rf: RequestFactory):
        """
        GIVEN a GET request of an instance of OrganisationView, and a user
        WHEN  displaying the list view
        THEN  context dictionnary should contain key 'organisations' and 'form'
        """
        request = rf.get("/fake-url/")
        request.user = user

        response = organisation_view(request)
        assert response.status_code == 200

        assert isinstance(response.context_data, dict)
        assert "organisations" in response.context_data
        assert "form" in response.context_data
        assert isinstance(response.context_data["form"], OrganisationForm)

    @pytest.mark.skip(reason="test not implemented yet")
    def test_delete_button(self, staff: User, organisation: Organisation, client):
        """
        GIVEN one organistion, and a staff member
        WHEN  display the list view
        THEN  one delete button should be display
        """
        url = reverse("organisations:list")
        client.force_login(staff)
        response = client.get(url)

        assertContains(response, f'href="/organisations/~delete/{organisation.id}/"', 1)
        assertContains(response, 'class="btn btn-danger"', 1)

    @pytest.mark.skip(reason="test not implemented yet")
    def test_no_delete_button(self, user: User, organisation: Organisation, client):
        """
        GIVEN one organistion, and a user (not in staff)
        WHEN  display the list view
        THEN  no delete button should be display
        """
        url = reverse("organisations:list")
        client.force_login(user)
        response = client.get(url)

        assertContains(response, f'href="/organisations/~delete/{organisation.id}/"', 0)
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
class TestOrganisationCreateView:
    def dummy_get_response(self, request: HttpRequest):
        return None

    def test_template(self, user: User, client):
        url = reverse("organisations:list")
        client.force_login(user)
        response = client.post(url)
        assertTemplateUsed(response, "organisations/organisation_list.html")

    def test_context_data(self, user: User, rf: RequestFactory):
        """
        GIVEN a POST request of an instance of OrganisationView, and a user
        WHEN  displaying the list view
        THEN  context dictionnary should contain key 'organisations' and 'form'
        """
        request = rf.post("/fake-url/")
        # Add the session/message middleware to the request
        SessionMiddleware(self.dummy_get_response).process_request(request)
        MessageMiddleware(self.dummy_get_response).process_request(request)
        request.user = user

        response = organisation_view(request)
        assert response.status_code == 200

        assert isinstance(response.context_data, dict)
        assert "organisations" in response.context_data
        assert "form" in response.context_data
        assert isinstance(response.context_data["form"], OrganisationForm)

    def test_context_form(self, user: User, organisation: Organisation, client):
        url = reverse("organisations:list")
        client.force_login(user)
        response = client.get(url)

        form = response.context.get("form")

        assert isinstance(form, OrganisationForm)

    def test_csrf(self, user: User, rf: RequestFactory):
        request = rf.get("/fake-url/")
        request.user = user

        response = organisation_view(request)

        assertContains(response, "csrfmiddlewaretoken")

    def test_form_buttons(self, user: User, client):
        """ """
        url = reverse("organisations:list")
        client.force_login(user)
        response = client.get(url)

        assertContains(response, 'input type="submit"', 1)

    def test_form_valid(self, user: User, rf: RequestFactory):
        """
        GIVEN an instance of OrganisationCreateView
          and a user (with an organisation)
        WHEN  posting an OrganisationForm
         with a new company name
        THEN  the form should be valid
          and a success message should appear
        """
        view = OrganisationCreateView()
        request = rf.get("/fake-url/")

        # Add the session/message middleware to the request
        SessionMiddleware(self.dummy_get_response).process_request(request)
        MessageMiddleware(self.dummy_get_response).process_request(request)
        request.user = user

        # view.request = request
        view.setup(request)

        # Initialize the form
        data = {"name": "another company"}
        form = OrganisationForm(data)
        form.cleaned_data = []
        assert form.is_valid()
        view.form_valid(form)

        messages_sent = [m.message for m in messages.get_messages(request)]
        assert messages_sent == ["Organisation 'another company' successfully added"]

    def test_form_invalid(self, user: User, rf: RequestFactory):
        """
        GIVEN an instance of OrganisationCreateView
          and a user (with an organisation)
        WHEN  posting an OrganisationForm
         with a company name already in use
        THEN  the form should be invalid
          and an error message should appear
        """
        view = OrganisationCreateView()
        request = rf.get("/fake-url/")

        # Add the session/message middleware to the request
        SessionMiddleware(self.dummy_get_response).process_request(request)
        MessageMiddleware(self.dummy_get_response).process_request(request)
        request.user = user

        view.setup(request)

        # Initialize the form
        data = {"name": user.organisation.name.lower()}
        form = OrganisationForm(data)
        form.cleaned_data = []
        assert not form.is_valid()

        view.form_invalid(form)

        messages_sent = [m.message for m in messages.get_messages(request)]
        assert messages_sent == ["An organisation with that name already exists."]

    @pytest.mark.skip(reason="test not implemented yet")
    def test_get_next_page(self, user: User, rf: RequestFactory):
        """
        GIVEN an instance of OrganisationCreateView,
          and a user (with an organisation)
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
    def test_success_url(self, user: User, rf: RequestFactory):
        """
        GIVEN an instance of OrganisationCreateView,
          and a user (with an organisation)
        WHEN
        THEN  should redirect to the organisations list url

        1. next_page from get_next_page is None
        1.1 run super().get_success_url()
        """
        view = OrganisationCreateView()
        request = rf.get("/fake-url/")
        request.user = user

        form = OrganisationForm()
        form.cleaned_data = []

        view.setup(request)
        view.next_page = None
        url = view.get_success_url()
        success_url = reverse("organisations:list")

        assert url == success_url


@pytest.mark.django_db
class TestOrganisationDeleteView:
    def dummy_get_response(self, request: HttpRequest):
        return None

    def test_template(self, user: User, client):
        """
        GIVEN an instance of OrganisationDeleteView,
          and a user (with an organisation)
        WHEN  requesting the deletion of an organisation
        THEN  should return the confirm_delete template
        """
        organisation = user.organisation
        url = reverse("organisations:delete", kwargs={"pk": organisation.id})
        client.force_login(user)
        response = client.get(url)
        assertTemplateUsed(response, "organisations/organisation_confirm_delete.html")

    def test_success_message(self, user: User, rf: RequestFactory):
        """
        GIVEN an instance of OrganisationDeleteView,
          and a user (with an organisation)
        WHEN  deleting successfuly the organisation
        THEN  should return a success message
        """
        organisation = user.organisation
        request = rf.delete("/fake-url/")

        # Add the session/message middleware to the request
        SessionMiddleware(self.dummy_get_response).process_request(request)
        MessageMiddleware(self.dummy_get_response).process_request(request)
        request.user = user

        OrganisationDeleteView.as_view()(request, pk=organisation.id)

        messages_sent = [m.message for m in messages.get_messages(request)]
        assert messages_sent == [
            f"Organisation '{organisation.name}' successfully removed"
        ]

    def test_delete_from_db(self, user: User, client):
        """
        GIVEN an instance of OrganisationDeleteView,
          and a user (with an organisation)
        WHEN  deleting successfuly the organisation
        THEN  databse should not contain any organisation
        """
        organisation = user.organisation
        url = reverse("organisations:delete", kwargs={"pk": organisation.id})
        client.force_login(user)
        client.delete(url)

        assert Organisation.objects.count() == 0

    def test_redirect_client(self, user: User, client):
        """
        GIVEN an instance of OrganisationDeleteView,
          and a user (with an organisation)
        WHEN  deleting successfuly the organisation
        THEN  should be redirect to organisations list page,
         with  status code 302
        """
        organisation = user.organisation
        url = reverse("organisations:delete", kwargs={"pk": organisation.id})
        client.force_login(user)
        response = client.delete(url, follow=True)
        success_url = reverse("organisations:list")

        redirect_url = response.redirect_chain[-1][0]
        redirect_status_code = response.redirect_chain[-1][1]
        assert redirect_url == f"{success_url}"
        assert redirect_status_code == 302

    def test_redirect(self, user: User, rf: RequestFactory):
        """
        GIVEN an instance of OrganisationDeleteView,
          and a user (with an organisation)
        WHEN  deleting successfuly the organisation
        THEN  should be redirect to organisations list page,
         with  status code 302
        """
        organisation = user.organisation
        request = rf.delete("/fake-url/")
        request.user = user
        # Add the session/message middleware to the request
        SessionMiddleware(self.dummy_get_response).process_request(request)
        MessageMiddleware(self.dummy_get_response).process_request(request)

        response = OrganisationDeleteView.as_view()(request, pk=organisation.id)
        success_url = reverse("organisations:list")

        assert response.status_code == 302
        assert response.url == f"{success_url}"

    @pytest.mark.skip(reason="test not implemented yet")
    def test_redirect_error(self, user: User, rf: RequestFactory):
        """
        GIVEN
        WHEN
        THEN
        """
        pass

    def test_get_not_authenticated(self, user: User, rf: RequestFactory):
        request = rf.get("/fake-url/")
        request.user = AnonymousUser()

        response = organisation_view(request)
        login_url = reverse(settings.LOGIN_URL)

        assert response.status_code == 302
        assert response.url == f"{login_url}?next=/fake-url/"

    @pytest.mark.skip(reason="test not implemented yet")
    def test_user_permission(self, user: User, rf: RequestFactory):
        """
        GIVEN
        WHEN
        THEN
        a no staff member should not be able to delete organisation
        """
        pass
