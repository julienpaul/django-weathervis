# Stdlib imports
# Core Django imports
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.gis.geos import Point as GeoPoint
from django.contrib.messages.views import SuccessMessageMixin
from django.core.serializers import serialize
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
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
from src.campaigns.models import Campaign
from src.domains.models import Domain
from src.utils import util

from .forms import StationCampaignForm, StationForm, StationUpdateForm
from .models import Station


def get_my_queryset(request):
    campaign_id = request.session.get("campaign_id")
    if campaign_id:
        qs = Station.objects.filter(campaigns=campaign_id)
    else:
        qs = Station.objects.all()

    return qs


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
        get_my_queryset(request),
    )
    # station = serialize("geojson", Station.objects.exclude(slug=slug))
    return HttpResponse(station, content_type="json")


@login_required
@permission_required("stations.change_station")
def disable_all_stations(request):
    """disable all station and return list view"""
    campaign_id = request.session.get("campaign_id", None)
    Station.disable_all(campaign_id)
    return redirect(reverse_lazy("stations:redirect"))


@login_required
@permission_required("stations.change_station")
def enable_all_stations(request):
    """enable all station and return list view"""
    campaign_id = request.session.get("campaign_id", None)
    Station.enable_all(campaign_id)
    return redirect(reverse_lazy("stations:redirect"))


@login_required
@permission_required("stations.change_station")
def download_config(request):
    """download config files for Station and return list view"""
    qs = get_my_queryset(request)
    station = qs.order_by("name").first()
    station.save()
    messages.info(request, "Stations config file successfully downloaded")
    return redirect(reverse_lazy("stations:redirect"))


class StationDetailListView(LoginRequiredMixin, SuccessMessageMixin, ListView):
    # based on https://stackoverflow.com/a/54461397
    model = Station
    template_name = "stations/station_detail_list.html"
    context_object_name = "stations"
    detail_context_object_name = "object"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def get_queryset_for_object(self):
        qs = self.get_queryset()
        return qs
        # raise NotImplementedError('You need to provide the queryset for the object')

    def get_object(self):
        queryset = self.get_queryset_for_object()
        slug = self.kwargs.get("slug")
        if slug is None:
            raise AttributeError("slug expected in url")
        return get_object_or_404(queryset, slug=slug)

    def get_context_data(self, **kwargs):
        _pk = self.request.session.get("campaign_id", None)
        if _pk:
            _campaign = Campaign.objects.get(pk=_pk)
            data = {
                "campaigns": [
                    _campaign,
                ]
            }
            form = StationCampaignForm(data)
        else:
            form = StationCampaignForm()

        context = super().get_context_data(**kwargs)
        station_url = {
            "station-add": reverse_lazy("stations:create"),
            "station-detail": reverse_lazy("stations:detail", kwargs={"slug": "dummy"}),
            "station-redirect": reverse_lazy("stations:redirect"),
            #     "stations:redirect", kwargs={"slug": "dummy"}
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
        context[self.detail_context_object_name] = self.object
        context["form"] = form
        return context


station_detail_list_view = StationDetailListView.as_view()


class StationCampaignDetailListView(StationDetailListView):
    def get_queryset(self):
        return get_my_queryset(self.request)
        # raise NotImplementedError('You need to provide the queryset for the object')


station_campaign_detail_list_view = StationCampaignDetailListView.as_view()


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
            "station-redirect": reverse_lazy("stations:redirect"),
            #     "stations:redirect", kwargs={"slug": "dummy"}
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
            "station-redirect": reverse_lazy("stations:redirect"),
            #    "stations:redirect", kwargs={"slug": "dummy"}
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
            "station-redirect": reverse_lazy("stations:redirect")
            #     "stations:redirect", kwargs={"slug": "dummy"}
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
        # url = reverse_lazy("stations:detail", kwargs={"slug": obj.slug})
        pk = obj.active_campaign
        if pk:
            url = reverse_lazy(
                "stations:campaign_detail_list", kwargs={"pk": pk, "slug": obj.slug}
            )
        else:
            url = reverse_lazy("stations:detail_list", kwargs={"slug": obj.slug})

        return url

    def get_success_message(self, clean_data):
        messages.info(self.request, "Stations config file successfully updtaed")
        return super().get_success_message(clean_data)


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

        active_campaign = self.request.session.get("campaign_id", None)
        data = {
            "latitude": _lat,
            "longitude": _lon,
            "altitude": _alt,
            "campaigns": active_campaign,
        }
        initial.update(data)
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        station_url = {
            "station-add": reverse_lazy("stations:create"),
            "station-detail": reverse_lazy("stations:detail", kwargs={"slug": "dummy"}),
            "station-redirect": reverse_lazy("stations:redirect"),
            #     "stations:redirect", kwargs={"slug": "dummy"}
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

        # add active campaign
        _campaign_id = self.request.session.get("campaign_id", None)
        if not _campaign_id:
            _campaign_id = None
        instance.active_campaign = _campaign_id

        # add margin geom
        margin = form.cleaned_data.get("margin")
        instance.margin_geom = util.margin2polygon(lon, lat, alt, margin)

        return super().form_valid(form)

    def get_success_url(self):
        obj = self.object
        # url = reverse_lazy("stations:detail", kwargs={"slug": obj.slug})
        pk = obj.active_campaign
        if pk:
            url = reverse_lazy(
                "stations:campaign_detail_list", kwargs={"pk": pk, "slug": obj.slug}
            )
        else:
            url = reverse_lazy("stations:detail_list", kwargs={"slug": obj.slug})

        return url

    def get_success_message(self, clean_data):
        messages.info(self.request, "Stations config file successfully updated")
        return super().get_success_message(clean_data)


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
    success_url = reverse_lazy("stations:redirect")

    def delete(self, request, *args, **kwargs):
        """ """
        # SuccessMessageMixin hooks to form_valid
        # which is not present on DeleteView to push its message to the user.
        # see https://stackoverflow.com/questions/24822509/success-message-in-deleteview-not-shown
        obj = self.get_object()
        messages.info(self.request, "Stations config file successfully updated")
        messages.success(self.request, self.success_message % obj.__dict__)
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        station_url = {
            "station-add": reverse_lazy("stations:create"),
            "station-detail": reverse_lazy("stations:detail", kwargs={"slug": "dummy"}),
            "station-redirect": reverse_lazy("stations:redirect"),
            # "stations:redirect", kwargs={"slug": "dummy"}
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
    """redirect to object detail page"""

    def get_redirect_url(self, *args, **kwargs):
        obj = None

        # look for session variable
        _campaign_id = self.request.session.get("campaign_id", None)
        if _campaign_id:
            if not obj:
                try:
                    self.pattern_name = "stations:campaign_detail_list"
                    obj = (
                        Station.objects.filter(campaigns=_campaign_id)
                        .order_by("name")
                        .first()
                    )
                    kwargs["slug"] = obj.slug
                except Exception:
                    self.pattern_name = "stations:create"
                else:
                    kwargs["pk"] = _campaign_id

        else:
            if not obj:
                try:
                    self.pattern_name = "stations:detail_list"
                    obj = Station.objects.order_by("name").first()
                    kwargs["slug"] = obj.slug
                except Exception:
                    self.pattern_name = "stations:create"

        return super().get_redirect_url(*args, **kwargs)


# class StationRedirectView(
#     LoginRequiredMixin,
#     RedirectView,
# ):
#     """redirect to plot object detail page"""
#
#     def get_redirect_url(self, slug, *args, **kwargs):
#         # _station = self.get_object(slug=slug)
#         _station = get_object_or_404(Station, slug=slug)
#         # look for session variable
#         if _station:
#             # if station object defined
#             _type = VMType.objects.get(Q(name="op1"))
#             _location = _station
#             _date = VMDate.objects.earliest("date")
#             #
#             data = {"type": _type, "location": _location, "date": _date}
#             form = VerticalMeteogramForm(data)
#             if form.is_valid():
#                 obj, created = VerticalMeteogram.objects.get_or_create(
#                     type=_type,
#                     location=_location,
#                     date=_date,
#                 )
#                 self.pattern_name = "vmeteograms:detail"
#                 kwargs["slug"] = obj.slug
#
#         # if not obj:
#
#         return super().get_redirect_url(*args, **kwargs)


station_redirect_view = StationRedirectView.as_view()


def change_campaign(request):
    """ """
    _campaign = None
    try:
        campaign_id = request.GET.get("campaigns", None)
        if campaign_id:
            _campaign = Campaign.objects.get(pk=campaign_id)
    except Campaign.DoesNotExist:
        pass

    data = {"campaign": _campaign}
    form = StationCampaignForm(data)
    if form.is_valid():
        data = {}
        # save location, and date
        request.session["campaign_id"] = campaign_id
        # update active campaign in database
        if campaign_id:
            Station.active_campaign_is(campaign_id)
            Domain.active_campaign_is(campaign_id)
        else:
            Station.active_campaign_is(None)
            Domain.active_campaign_is(None)

        # data["url"] = reverse("stations:campaign_detail", kwargs={"pk": _campaign.pk, "slug":})
        data["url"] = reverse("stations:redirect")
        return JsonResponse(data)
    else:
        return render(request, "stations/station_detail_list.html", {"form": form})
