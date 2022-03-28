# Stdlib imports
# Core Django imports
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.gis.geos import Point as GeoPoint
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from src.utils import util

# Third-party app imports
# Imports from my apps
from src.utils.mixins import DrawMapMixin

from .forms import StationForm, StationUpdateForm
from .models import Station


class StationListView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    DrawMapMixin,
    ListView,
):
    model = Station
    template_name = "stations/station_list.html"
    context_object_name = "stations"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        m = self.draw_map()
        context["map"] = m._repr_html_()
        context["form"] = StationForm()
        return context


station_list_view = StationListView.as_view()


class StationDetailView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    DrawMapMixin,
    DetailView,
):
    model = Station
    context_object_name = "station"
    slug_field = "slug"
    template_name = "stations/station_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        m = self.draw_map(local=self.object)
        context["map"] = m._repr_html_()
        context["form"] = StationForm()
        return context


station_detail_view = StationDetailView.as_view()


class StationUpdateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    SuccessMessageMixin,
    DrawMapMixin,
    UpdateView,
):
    permission_required = "stations.change_station"
    model = Station
    context_object_name = "stations"
    slug_field = "slug"
    form_class = StationUpdateForm
    # template_name = "domain/station_detail.html"
    success_message = _("Station '%(name)s' successfully updated")

    def get_initial(self):
        initial = super().get_initial()
        # update initial field defaults with custom set default values:
        obj = self.object
        data = {
            "name": obj.name,
            "latitude": obj.latitude,
            "longitude": obj.longitude,
            "altitude": obj.altitude,
            "station_id": obj.station_id,
            "wmo_id": obj.wmo_id,
            "description": obj.description,
            "margin": obj.margin,
            "is_active": obj.is_active,
        }
        initial.update(data)
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        m = self.draw_map(local=self.object)
        context["map"] = m._repr_html_()
        return context

    def form_valid(self, form):
        # Here, add geometry using lon, lat
        # passed in form.cleaned_data['message']
        instance = form.save(commit=False)
        # capitalize name
        instance.name = form.cleaned_data.get("name").capitalize()
        lat = float(form.cleaned_data.get("latitude", 0))
        lon = float(form.cleaned_data.get("longitude", 0))
        alt = float(form.cleaned_data.get("altitude", 0))
        instance.geom = GeoPoint(lon, lat, alt)

        # add margin geom
        margin = form.cleaned_data.get("margin")
        instance.margin_geom = util.margin2polygon(lon, lat, alt, margin)

        return super().form_valid(form)

    def get_success_url(self):
        obj = self.object
        url = reverse_lazy("stations:detail", kwargs={"slug": obj.slug})

        return url


station_update_view = StationUpdateView.as_view()


class StationCreateView(
    PermissionRequiredMixin,
    LoginRequiredMixin,
    SuccessMessageMixin,
    DrawMapMixin,
    CreateView,
):
    permission_required = "stations.change_station"
    model = Station
    form_class = StationForm
    context_object_name = "stations"
    template_name = "stations/station_create.html"

    success_message = _("Station '%(name)s' successfully added")
    success_url = reverse_lazy("stations:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        m = self.draw_map(local=self.object)
        context["map"] = m._repr_html_()
        return context

    def form_valid(self, form):
        # Here, add geometry using lon, lat
        # passed in form.cleaned_data['message']
        instance = form.save(commit=False)
        # capitalize name
        instance.name = form.cleaned_data.get("name").capitalize()
        lat = float(form.cleaned_data.get("latitude", 0))
        lon = float(form.cleaned_data.get("longitude", 0))
        alt = float(form.cleaned_data.get("altitude", 0))
        instance.geom = GeoPoint(lon, lat, alt)

        # add margin geom
        margin = form.cleaned_data.get("margin")
        instance.margin_geom = util.margin2polygon(lon, lat, alt, margin)

        return super().form_valid(form)


station_create_view = StationCreateView.as_view()


class StationDeleteView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    SuccessMessageMixin,
    DrawMapMixin,
    DeleteView,
):
    permission_required = "stations.delete_station"
    model = Station
    slug_field = "slug"

    success_message = _("Station '%(name)s' successfully removed")
    success_url = reverse_lazy("stations:list")

    def delete(self, request, *args, **kwargs):
        """ """
        # SuccessMessageMixin hooks to form_valid
        # which is not present on DeleteView to push its message to the user.
        # see https://stackoverflow.com/questions/24822509/success-message-in-deleteview-not-shown
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        m = self.draw_map(local=self.object)
        context["map"] = m._repr_html_()
        return context


station_confirm_delete_view = StationDeleteView.as_view()
