# Stdlib imports
# Core Django imports
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.gis.geos import Point as GeoPoint
from django.contrib.messages.views import SuccessMessageMixin
from django.core.serializers import serialize
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    RedirectView,
    UpdateView,
)

# Third-party app imports
# Imports from my apps
from src.utils import util
from src.vertical_meteograms.forms import VerticalMeteogramForm
from src.vertical_meteograms.models import VerticalMeteogram, VMDate, VMType

from .forms import StationForm, StationUpdateForm
from .models import Station


def data_this_station_margin(request, slug):
    """this uses the serializer to convert the data 'Station.objects.all()' to 'geojson' data"""
    station = serialize(
        "geojson",
        Station.objects.filter(slug=slug),
        geometry_field=("margin_geom"),
    )
    return HttpResponse(station, content_type="json")


def data_all_stations(request, slug=None):
    """this uses the serializer to convert the data 'Station.objects.all()' to 'geojson' data"""
    station = serialize(
        "geojson",
        Station.objects.all(),
    )
    # station = serialize("geojson", Station.objects.exclude(slug=slug))
    return HttpResponse(station, content_type="json")


class StationListView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    ListView,
):
    model = Station
    template_name = "stations/station_list.html"
    context_object_name = "stations"
    paginate_by = 14

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        station_url = {
            "station-add": reverse_lazy("stations:create"),
            "station-detail": reverse_lazy("stations:detail", kwargs={"slug": "dummy"}),
            "station-redirect": reverse_lazy(
                "stations:redirect", kwargs={"slug": "dummy"}
            ),
        }
        station_data = {
            "station-all": reverse_lazy("stations:all_stations"),
        }
        grid_data = {
            "grid-all": reverse_lazy("model_grids:all_grids"),
        }

        context["station_url"] = station_url
        context["station_data"] = station_data
        context["grid_data"] = grid_data
        context["form"] = StationForm()
        return context


station_list_view = StationListView.as_view()


class StationDetailView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    DetailView,
):
    model = Station
    context_object_name = "station"
    slug_field = "slug"
    template_name = "stations/station_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        station_url = {
            "station-add": reverse_lazy("stations:create"),
            "station-detail": reverse_lazy("stations:detail", kwargs={"slug": "dummy"}),
            "station-redirect": reverse_lazy(
                "stations:redirect", kwargs={"slug": "dummy"}
            ),
        }
        station_data = {
            "station-local": self.object.slug,
            "station-all": reverse_lazy("stations:all_stations"),
            "margin_local": reverse_lazy(
                "stations:this_margin", kwargs={"slug": self.object.slug}
            ),
        }
        grid_data = {
            "grid-all": reverse_lazy("model_grids:all_grids"),
        }

        context["station_url"] = station_url
        context["station_data"] = station_data
        context["grid_data"] = grid_data
        context["form"] = StationForm()
        return context


station_detail_view = StationDetailView.as_view()


class StationUpdateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    SuccessMessageMixin,
    UpdateView,
):
    permission_required = "stations.change_station"
    model = Station
    context_object_name = "station"
    slug_field = "slug"
    form_class = StationUpdateForm
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
        station_url = {
            "station-add": reverse_lazy("stations:create"),
            "station-detail": reverse_lazy("stations:detail", kwargs={"slug": "dummy"}),
            "station-redirect": reverse_lazy(
                "stations:redirect", kwargs={"slug": "dummy"}
            ),
        }
        station_data = {
            "station-local": self.object.slug,
            "station-all": reverse_lazy("stations:all_stations"),
            "margin_local": reverse_lazy(
                "stations:this_margin", kwargs={"slug": self.object.slug}
            ),
        }
        grid_data = {
            "grid-all": reverse_lazy("model_grids:all_grids"),
        }

        context["station_url"] = station_url
        context["station_data"] = station_data
        context["grid_data"] = grid_data
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
    CreateView,
):
    permission_required = "stations.change_station"
    model = Station
    form_class = StationForm
    context_object_name = "stations"
    template_name = "stations/station_create.html"

    success_message = _("Station '%(name)s' successfully added")
    success_url = reverse_lazy("stations:list")

    def get_initial(self):
        initial = super().get_initial()
        # update initial field defaults with custom set default values:
        _lat = self.request.GET.get("latitude", None)
        if _lat is not None:
            try:
                _lat = float(_lat)
            except Exception:
                raise ValueError(f"latitude {_lat} must be a float {type(_lat)}")

        _lon = self.request.GET.get("longitude", None)
        if _lon is not None:
            try:
                _lon = float(_lon)
            except Exception:
                raise ValueError(f"longitude {_lon} must be a float {type(_lon)}")

        if None in [_lat, _lon]:
            _lat, _lon, _alt = None, None, None
        else:
            _alt = 0.0

        data = {
            "latitude": _lat,
            "longitude": _lon,
            "altitude": _alt,
        }
        initial.update(data)
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        station_url = {
            "station-add": reverse_lazy("stations:create"),
            "station-detail": reverse_lazy("stations:detail", kwargs={"slug": "dummy"}),
            "station-redirect": reverse_lazy(
                "stations:redirect", kwargs={"slug": "dummy"}
            ),
        }
        station_data = {
            "station-all": reverse_lazy("stations:all_stations"),
        }
        grid_data = {
            "grid-all": reverse_lazy("model_grids:all_grids"),
        }

        context["station_url"] = station_url
        context["station_data"] = station_data
        context["grid_data"] = grid_data
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
    DeleteView,
):
    permission_required = "stations.delete_station"
    model = Station
    context_object_name = "station"
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
        station_url = {
            "station-add": reverse_lazy("stations:create"),
            "station-detail": reverse_lazy("stations:detail", kwargs={"slug": "dummy"}),
            "station-redirect": reverse_lazy(
                "stations:redirect", kwargs={"slug": "dummy"}
            ),
        }
        station_data = {
            "station-local": self.object.slug,
            "station-all": reverse_lazy("stations:all_stations"),
            "margin_local": reverse_lazy(
                "stations:this_margin", kwargs={"slug": self.object.slug}
            ),
        }
        grid_data = {
            "grid-all": reverse_lazy("model_grids:all_grids"),
        }

        context["station_url"] = station_url
        context["station_data"] = station_data
        context["grid_data"] = grid_data
        return context


station_confirm_delete_view = StationDeleteView.as_view()


class StationRedirectView(
    LoginRequiredMixin,
    RedirectView,
):
    """redirect to plot object detail page"""

    def get_redirect_url(self, slug, *args, **kwargs):
        # _station = self.get_object(slug=slug)
        _station = get_object_or_404(Station, slug=slug)
        # look for session variable
        if _station:
            # if station object defined
            _type = VMType.objects.get(Q(name="op1"))
            _location = _station
            _date = VMDate.objects.earliest("date")
            #
            data = {"type": _type, "location": _location, "date": _date}
            form = VerticalMeteogramForm(data)
            if form.is_valid():
                obj, created = VerticalMeteogram.objects.get_or_create(
                    type=_type,
                    location=_location,
                    date=_date,
                )
                self.pattern_name = "vmeteograms:detail"
                kwargs["slug"] = obj.slug

        # if not obj:

        return super().get_redirect_url(*args, **kwargs)


station_redirect_view = StationRedirectView.as_view()
