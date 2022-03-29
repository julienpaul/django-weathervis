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
from src.model_grids.models import ModelGrid
from src.stations.forms import StationForm
from src.stations.models import Station
from src.stations.views import (
    StationCreateView,
    StationDeleteView,
    StationDetailView,
    StationListView,
    StationUpdateView,
    station_confirm_delete_view,
    station_create_view,
    station_detail_view,
    station_list_view,
    station_update_view,
)
from src.users.models import User


@pytest.mark.django_db
class TestStationListView:
    def test_get_authenticated(self, rf: RequestFactory, user: User):
        request = rf.get("/fake-url/")
        request.user = user

        response = station_list_view(request)
        assert response.status_code == 200

        # Use this syntax for class-based views.
        response = StationListView.as_view()(request)
        assert response.status_code == 200

    def test_get_not_authenticated(self, rf: RequestFactory):
        request = rf.get("/fake-url/")
        request.user = AnonymousUser()

        response = station_list_view(request)
        login_url = reverse(settings.LOGIN_URL)

        assert response.status_code == 302
        assert response.url == f"{login_url}?next=/fake-url/"

    def test_get_template(self, user: User, client):
        url = reverse("stations:list")
        client.force_login(user)
        response = client.get(url)
        assertTemplateUsed(response, "stations/station_list.html")

    @pytest.mark.skip(reason="test not implemented yet")
    def test_pagination(self):
        """
        GIVEN N stations
        WHEN  display the list view
        THEN  should see X pages
        """
        pass

    def test_context_data(self, rf: RequestFactory, user: User):
        """
        GIVEN a GET request of an instance of StationListView, and a user
        WHEN  displaying the list view
        THEN  context dictionnary should contain key 'map' and 'form'
        """
        request = rf.get("/fake-url/")
        request.user = user

        response = station_list_view(request)
        assert response.status_code == 200

        assert isinstance(response.context_data, dict)
        assert "map" in response.context_data
        # assert isinstance(response.context_data["map"], FoliumMap)
        assert "form" in response.context_data
        assert isinstance(response.context_data["form"], StationForm)

    def test_staff_create_button(self, client, staff: User):
        """
        GIVEN a staff member
        WHEN  display the list view
        THEN  one create button should be display
        """
        url = reverse("stations:list")
        client.force_login(staff)
        response = client.get(url)

        assertContains(response, 'href="/stations/~add/"', 1)
        assertContains(response, 'class="btn btn-primary"', 1)

    @pytest.mark.skip(reason="test not implemented yet")
    def test_user_no_create_button(self, client, user: User):
        """
        GIVEN a standard user
        WHEN  display the list view
        THEN  no create button should be display
        """
        url = reverse("stations:list")
        client.force_login(user)
        response = client.get(url)

        assertContains(response, 'href="/stations/~add/"', 0)
        assertContains(response, 'class="btn btn-primary"', 0)

    @pytest.mark.parametrize("user", [{"groups": "Editor"}], indirect=True)
    def test_editor_station_buttons(self, client, user: User, station: Station):
        """
        GIVEN one station,
          and  a user, from group 'Editor'
        WHEN  display the list view
        THEN  three buttons (detail/update/delete) should be displayed
         and  delete button should be disabled
        """
        url = reverse("stations:list")
        client.force_login(user)
        response = client.get(url)

        # detail
        assertContains(response, f'href="/stations/{station.slug}/"', 1)
        # two primary buttons, detail and create
        assertContains(response, 'class="btn btn-primary"', 2)
        # update
        assertContains(response, f'href="/stations/{station.slug}/~update/"', 1)
        assertContains(response, 'class="btn btn-success"', 1)
        # delete
        assertContains(response, f'href="/stations/~delete/{station.slug}/"', 1)
        assertContains(response, 'class="btn btn-secondary"', 1)

    def test_staff_station_buttons(self, client, staff: User, station: Station):
        """
        GIVEN one station,
          and a staff member
        WHEN  display the list view
        THEN  three buttons (detail/update/delete) should be displayed
        """
        url = reverse("stations:list")
        client.force_login(staff)
        response = client.get(url)

        # detail
        assertContains(response, f'href="/stations/{station.slug}/"', 1)
        # two primary buttons, detail and create
        assertContains(response, 'class="btn btn-primary"', 2)
        # update
        assertContains(response, f'href="/stations/{station.slug}/~update/"', 1)
        assertContains(response, 'class="btn btn-success"', 1)
        # delete
        assertContains(response, f'href="/stations/~delete/{station.slug}/"', 1)
        assertContains(response, 'class="btn btn-danger"', 1)

    @pytest.mark.skip(reason="test not implemented yet")
    def test_user_station_buttons(self, client, staff: User, station: Station):
        """
        GIVEN one station,
          and a standard user
        WHEN  display the list view
        THEN  one button detail should be displayed
              update and delete should be hiden
        """
        url = reverse("stations:list")
        client.force_login(staff)
        response = client.get(url)

        # detail
        assertContains(response, f'href="/stations/{station.slug}/"', 1)
        assertContains(response, 'class="btn btn-primary"', 1)
        # update
        assertContains(response, f'href="/stations/{station.slug}/~update/"', 0)
        assertContains(response, 'class="btn btn-success"', 0)
        # delete
        assertContains(response, f'href="/stations/~delete/{station.slug}/"', 0)
        assertContains(response, 'class="btn btn-danger"', 0)


@pytest.mark.django_db
class TestStationDetailView:
    def dummy_get_response(self, request: HttpRequest):
        return None

    def test_get_authenticated(self, rf: RequestFactory, user: User, station: Station):
        request = rf.get("/fake-url/")
        request.user = user

        response = station_detail_view(request, slug=station.slug)
        assert response.status_code == 200

        # Use this syntax for class-based views.
        response = StationDetailView.as_view()(request, slug=station.slug)
        assert response.status_code == 200

    def test_get_not_authenticated(self, rf: RequestFactory, station: Station):
        request = rf.get("/fake-url/")
        request.user = AnonymousUser()

        response = station_detail_view(request, slug=station.slug)
        login_url = reverse(settings.LOGIN_URL)

        assert response.status_code == 302
        assert response.url == f"{login_url}?next=/fake-url/"

    def test_get_template(self, client, user: User, station: Station):
        url = reverse("stations:detail", kwargs={"slug": station.slug})
        client.force_login(user)
        response = client.get(url)
        assertTemplateUsed(response, "stations/station_detail.html")

    @pytest.mark.parametrize("user", [{"groups": "Editor"}], indirect=True)
    def test_context_data(self, rf: RequestFactory, user: User, station: Station):
        """
        GIVEN a POST request of an instance of StationDeatilView,
          and a user
        WHEN  displaying the create view
        THEN  context dictionnary should contain key 'map'
        """
        request = rf.post("/fake-url/")
        # Add the session/message middleware to the request
        SessionMiddleware(self.dummy_get_response).process_request(request)
        MessageMiddleware(self.dummy_get_response).process_request(request)
        request.user = user

        response = station_update_view(request, slug=station.slug)
        assert response.status_code == 200

        assert isinstance(response.context_data, dict)
        assert "map" in response.context_data


@pytest.mark.django_db
class TestStationUpdateView:
    def dummy_get_response(self, request: HttpRequest):
        return None

    @pytest.mark.parametrize("user", [{"groups": "Editor"}], indirect=True)
    def test_get_authenticated(self, rf: RequestFactory, user: User, station: Station):
        request = rf.get("/fake-url/")
        request.user = user

        response = station_update_view(request, slug=station.slug)
        assert response.status_code == 200

        # Use this syntax for class-based views.
        response = StationUpdateView.as_view()(request, slug=station.slug)
        assert response.status_code == 200

    def test_get_not_authenticated(self, rf: RequestFactory, station: Station):
        request = rf.get("/fake-url/")
        request.user = AnonymousUser()

        response = station_update_view(request, slug=station.slug)
        login_url = reverse(settings.LOGIN_URL)

        assert response.status_code == 302
        assert response.url == f"{login_url}?next=/fake-url/"

    @pytest.mark.parametrize("user", [{"groups": "Editor"}], indirect=True)
    def test_get_template(self, client, user: User, station: Station):
        url = reverse("stations:update", kwargs={"slug": station.slug})
        client.force_login(user)
        response = client.get(url)
        assertTemplateUsed(response, "stations/station_form.html")

    @pytest.mark.parametrize("user", [{"groups": "Editor"}], indirect=True)
    def test_context_data(self, rf: RequestFactory, user: User, station: Station):
        """
        GIVEN a POST request of an instance of StationUpdateView,
          and a user
        WHEN  displaying the create view
        THEN  context dictionnary should contain key 'map' and 'form'
        """
        request = rf.post("/fake-url/")
        # Add the session/message middleware to the request
        SessionMiddleware(self.dummy_get_response).process_request(request)
        MessageMiddleware(self.dummy_get_response).process_request(request)
        request.user = user

        response = station_update_view(request, slug=station.slug)
        assert response.status_code == 200

        assert isinstance(response.context_data, dict)
        assert "map" in response.context_data
        assert "form" in response.context_data
        assert isinstance(response.context_data["form"], StationForm)

    @pytest.mark.parametrize("user", [{"groups": "Editor"}], indirect=True)
    def test_context_form(self, client, user: User, station: Station):
        url = reverse("stations:update", kwargs={"slug": station.slug})
        client.force_login(user)
        response = client.get(url)

        form = response.context.get("form")

        assert isinstance(form, StationForm)

    @pytest.mark.parametrize("user", [{"groups": "Editor"}], indirect=True)
    def test_csrf(self, rf: RequestFactory, user: User, station: Station):
        request = rf.get("/fake-url/")
        request.user = user

        response = station_update_view(request, slug=station.slug)

        assertContains(response, "csrfmiddlewaretoken")

    @pytest.mark.parametrize("user", [{"groups": "Editor"}], indirect=True)
    def test_form_buttons(self, client, user: User, station: Station):
        """ """
        url = reverse("stations:update", kwargs={"slug": station.slug})
        client.force_login(user)
        response = client.get(url)

        assertContains(response, 'input type="submit"', 1)

    @pytest.mark.parametrize("user", [{"groups": "Editor"}], indirect=True)
    def test_form_valid(
        self,
        rf: RequestFactory,
        user: User,
        station: Station,
        modelGrid: ModelGrid,
    ):
        """
        GIVEN an instance of stationCreateView
          and a user
          and a station
          and a model_grid
        WHEN  posting an stationForm
         with a new station name
        THEN  the form should be valid
          and a success message should appear
        """
        centroid = modelGrid.geom.centroid
        _name = "another station"
        _lon = round(centroid.x, 6)
        _lat = round(centroid.y, 6)
        _alt = round(0, 6)

        # Initialize the form
        data = {
            "name": _name,
            "latitude": _lat,
            "longitude": _lon,
            "altitude": _alt,
            # "station_id": "any99",
            # "wmo_id": "any99",
            # "description": "blabla",
            # margin is a ForeignKey so we need to pass the object ID in data
            "margin": station.margin.pk,
        }

        view = StationUpdateView()
        request = rf.post("/fake-url/")

        # Add the session/message middleware to the request
        SessionMiddleware(self.dummy_get_response).process_request(request)
        MessageMiddleware(self.dummy_get_response).process_request(request)
        request.user = user

        # view.request = request
        view.setup(request)

        form = StationForm(data)
        form.cleaned_data = []

        assert form.is_valid()
        view.form_valid(form)

        messages_sent = [m.message for m in messages.get_messages(request)]
        assert messages_sent == [f"Station '{_name}' successfully updated"]

    @pytest.mark.skip(reason="test not implemented yet")
    def test_form_invalid(self):
        pass

    @pytest.mark.skip(reason="test not implemented yet")
    def test_get_next_page(self):
        pass

    @pytest.mark.skip(reason="test not working yet")
    def test_success_url(self, rf: RequestFactory, user: User, station: Station):
        view = StationUpdateView(slug=station.slug)
        request = rf.post("/fake-url")
        request.user = user

        view.setup(request)

        success_url = f"/stations/{station.slug}/"
        assert view.get_success_url() == success_url


@pytest.mark.django_db
class TestStationCreateView:
    def dummy_get_response(self, request: HttpRequest):
        return None

    @pytest.mark.parametrize("user", [{"groups": "Editor"}], indirect=True)
    def test_get_authenticated(self, rf: RequestFactory, user: User):
        request = rf.get("/fake-url/")
        request.user = user

        response = station_create_view(request)
        assert response.status_code == 200

        # Use this syntax for class-based views.
        response = StationCreateView.as_view()(request)
        assert response.status_code == 200

    def test_get_not_authenticated(self, rf: RequestFactory):
        request = rf.get("/fake-url/")
        request.user = AnonymousUser()

        response = station_create_view(request)
        login_url = reverse(settings.LOGIN_URL)

        assert response.status_code == 302
        assert response.url == f"{login_url}?next=/fake-url/"

    @pytest.mark.parametrize("user", [{"groups": "Editor"}], indirect=True)
    def test_get_template(self, client, user: User):
        url = reverse("stations:create")
        client.force_login(user)
        response = client.get(url)
        assertTemplateUsed(response, "stations/station_create.html")

    @pytest.mark.parametrize("user", [{"groups": "Editor"}], indirect=True)
    def test_context_data(self, rf: RequestFactory, user: User):
        """
        GIVEN a POST request of an instance of StationCreateView,
          and a user
        WHEN  displaying the create view
        THEN  context dictionnary should contain key 'map' and 'form'
        """
        request = rf.post("/fake-url/")
        # Add the session/message middleware to the request
        SessionMiddleware(self.dummy_get_response).process_request(request)
        MessageMiddleware(self.dummy_get_response).process_request(request)
        request.user = user

        response = station_create_view(request)
        assert response.status_code == 200

        assert isinstance(response.context_data, dict)
        assert "map" in response.context_data
        assert "form" in response.context_data
        assert isinstance(response.context_data["form"], StationForm)

    @pytest.mark.parametrize("user", [{"groups": "Editor"}], indirect=True)
    def test_context_form(self, client, user: User, station: Station):
        url = reverse("stations:create")
        client.force_login(user)
        response = client.get(url)

        form = response.context.get("form")

        assert isinstance(form, StationForm)

    @pytest.mark.parametrize("user", [{"groups": "Editor"}], indirect=True)
    def test_csrf(self, rf: RequestFactory, user: User):
        request = rf.get("/fake-url/")
        request.user = user

        response = station_create_view(request)

        assertContains(response, "csrfmiddlewaretoken")

    @pytest.mark.parametrize("user", [{"groups": "Editor"}], indirect=True)
    def test_form_buttons(self, client, user: User):
        """ """
        url = reverse("stations:create")
        client.force_login(user)
        response = client.get(url)

        assertContains(response, 'input type="submit"', 1)

    @pytest.mark.parametrize("user", [{"groups": "Editor"}], indirect=True)
    def test_form_valid(
        self,
        rf: RequestFactory,
        user: User,
        station: Station,
        modelGrid: ModelGrid,
    ):
        """
        GIVEN an instance of stationCreateView
          and a user
          and a station
          and a model_grid
        WHEN  posting an stationForm
         with a new station name
        THEN  the form should be valid
          and a success message should appear
        """
        view = StationCreateView()
        request = rf.get("/fake-url/")

        # Add the session/message middleware to the request
        SessionMiddleware(self.dummy_get_response).process_request(request)
        MessageMiddleware(self.dummy_get_response).process_request(request)
        request.user = user

        # view.request = request
        view.setup(request)

        centroid = modelGrid.geom.centroid
        _name = "another station"
        _lon = round(centroid.x, 6)
        _lat = round(centroid.y, 6)
        _alt = round(0, 6)

        # Initialize the form
        data = {
            "name": _name,
            "latitude": _lat,
            "longitude": _lon,
            "altitude": _alt,
            # "station_id": "any99",
            # "wmo_id": "any99",
            # "description": "blabla",
            # margin is a ForeignKey so we need to pass the object ID in data
            "margin": station.margin.pk,
        }

        form = StationForm(data)
        form.cleaned_data = []

        assert form.is_valid()
        view.form_valid(form)

        messages_sent = [m.message for m in messages.get_messages(request)]
        assert messages_sent == [f"Station '{_name}' successfully added"]

    @pytest.mark.parametrize("user", [{"groups": "Editor"}], indirect=True)
    def test_success_message_client(
        self,
        client,
        user: User,
        station: Station,
        modelGrid: ModelGrid,
    ):
        """
        GIVEN an instance of StationDeleteView,
          and a user
        WHEN  deleting successfuly the station
        THEN  should return a success message
        """
        centroid = modelGrid.geom.centroid
        _name = "another station"
        _lon = round(centroid.x, 6)
        _lat = round(centroid.y, 6)
        _alt = round(0, 6)

        # Initialize the form
        data = {
            "name": _name,
            "latitude": _lat,
            "longitude": _lon,
            "altitude": _alt,
            # "station_id": "any99",
            # "wmo_id": "any99",
            # "description": "blabla",
            # margin is a ForeignKey so we need to pass the object ID in data
            "margin": station.margin.pk,
        }

        url = reverse("stations:create")
        client.force_login(user)
        response = client.post(url, data=data, follow=True)

        assert response.status_code == 200
        messages_sent = [
            m.message for m in messages.get_messages(response.wsgi_request)
        ]
        assert messages_sent == [f"Station '{_name}' successfully added"]

    @pytest.mark.skip(reason="test not working yet")
    def test_success_message_rf(
        self,
        rf: RequestFactory,
        user: User,
        station: Station,
        modelGrid: ModelGrid,
    ):
        """
        GIVEN an instance of StationDeleteView,
          and a user
        WHEN  deleting successfuly the station
        THEN  should return a success message
        """
        centroid = modelGrid.geom.centroid
        _name = "another station"
        _lon = round(centroid.x, 6)
        _lat = round(centroid.y, 6)
        _alt = round(0, 6)

        # Initialize the form
        data = {
            "name": _name,
            "latitude": _lat,
            "longitude": _lon,
            "altitude": _alt,
            # "station_id": "any99",
            # "wmo_id": "any99",
            # "description": "blabla",
            # margin is a ForeignKey so we need to pass the object ID in data
            "margin": station.margin.pk,
        }

        request = rf.post("/fake-url/", data=data)
        request.user = user

        # Add the session/message middleware to the request
        SessionMiddleware(self.dummy_get_response).process_request(request)
        MessageMiddleware(self.dummy_get_response).process_request(request)

        view = StationCreateView(slug=station.slug)
        view.setup(request)

        messages_sent = [m.message for m in messages.get_messages(request)]
        assert messages_sent == [f"Station '{station.name}' successfully removed"]

    @pytest.mark.skip(reason="test not implemented yet")
    def test_form_invalid(self):
        pass

    @pytest.mark.skip(reason="test not implemented yet")
    def test_get_next_page(self):
        pass

    @pytest.mark.skip(reason="test not working yet")
    def test_success_url(self, rf: RequestFactory, user: User):
        view = StationCreateView()
        request = rf.post("/fake-url")
        request.user = user

        view.request = request

        success_url = reverse("stations:list")
        assert view.get_success_url() == success_url


@pytest.mark.django_db
class TestStationDeleteView:
    def dummy_get_response(self, request: HttpRequest):
        return None

    def test_get_authenticated(self, rf: RequestFactory, staff: User, station: Station):
        request = rf.get("/fake-url/")
        request.user = staff

        response = station_confirm_delete_view(request, slug=station.slug)
        assert response.status_code == 200

        # Use this syntax for class-based views.
        response = StationDeleteView.as_view()(request, slug=station.slug)
        assert response.status_code == 200

    def test_get_not_authenticated(self, rf: RequestFactory, station: Station):
        request = rf.get("/fake-url/")
        request.user = AnonymousUser()

        response = station_confirm_delete_view(request, slug=station.slug)
        login_url = reverse(settings.LOGIN_URL)

        assert response.status_code == 302
        assert response.url == f"{login_url}?next=/fake-url/"

    def test_get_template(self, client, staff: User, station: Station):
        """
        GIVEN an instance of StationDeleteView,
          and a staff member
        WHEN  requesting the deletion of a station
        THEN  should return the confirm_delete template
        """
        url = reverse("stations:delete", kwargs={"slug": station.slug})
        client.force_login(staff)
        response = client.get(url)
        assertTemplateUsed(response, "stations/station_confirm_delete.html")

    def test_csrf(self, rf: RequestFactory, staff: User, station: Station):
        request = rf.get("/fake-url/")
        request.user = staff

        response = station_confirm_delete_view(request, slug=station.slug)

        assertContains(response, "csrfmiddlewaretoken")

    def test_success_message(self, rf: RequestFactory, staff: User, station: Station):
        """
        GIVEN an instance of StationDeleteView,
          and a staff member
        WHEN  deleting successfuly the station
        THEN  should return a success message
        """
        request = rf.delete("/fake-url/")

        # Add the session/message middleware to the request
        SessionMiddleware(self.dummy_get_response).process_request(request)
        MessageMiddleware(self.dummy_get_response).process_request(request)
        request.user = staff

        StationDeleteView.as_view()(request, slug=station.slug)

        messages_sent = [m.message for m in messages.get_messages(request)]
        assert messages_sent == [f"Station '{station.name}' successfully removed"]

    def test_delete_from_db(self, client, staff: User, station: Station):
        """
        GIVEN an instance of StationDeleteView,
          and a staff member
        WHEN  deleting successfuly the station
        THEN  databse should not contain any station
        """
        url = reverse("stations:delete", kwargs={"slug": station.slug})
        client.force_login(staff)
        client.delete(url)

        assert Station.objects.count() == 0

    def test_redirect_client(self, client, staff: User, station: Station):
        """
        GIVEN an instance of StationDeleteView,
          and a staff member
          and a station
        WHEN  deleting successfuly the station
        THEN  should be redirect to stations list page,
         with  status code 302
        """
        url = reverse("stations:delete", kwargs={"slug": station.slug})
        client.force_login(staff)
        response = client.delete(url, follow=True)
        success_url = reverse("stations:list")

        redirect_url = response.redirect_chain[-1][0]
        redirect_status_code = response.redirect_chain[-1][1]
        assert redirect_url == f"{success_url}"
        assert redirect_status_code == 302

    def test_redirect(self, rf: RequestFactory, staff: User, station: Station):
        """
        GIVEN an instance of OrganisationDeleteView,
          and a staff member
          and a station
        WHEN  deleting successfuly the station
        THEN  should be redirect to stations list page,
         with  status code 302
        """
        request = rf.delete("/fake-url/")
        request.user = staff
        # Add the session/message middleware to the request
        SessionMiddleware(self.dummy_get_response).process_request(request)
        MessageMiddleware(self.dummy_get_response).process_request(request)

        response = StationDeleteView.as_view()(request, slug=station.slug)
        success_url = reverse("stations:list")

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

    @pytest.mark.skip(reason="test not implemented yet")
    def test_user_permission(self, rf: RequestFactory, user: User):
        """
        GIVEN
        WHEN
        THEN
        a no staff member should not be able to delete organisation
        """
        pass
