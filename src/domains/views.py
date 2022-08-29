# Stdlib imports
# Core Django imports
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.gis.geos import Polygon as GeoPolygon
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
from src.stations.models import Station

from .forms import DomainCampaignForm, DomainForm, DomainUpdateForm
from .models import Domain


def get_my_queryset(request):
    campaign_id = request.session.get("campaign_id")
    if campaign_id:
        qs = Domain.objects.filter(campaigns=campaign_id)
    else:
        qs = Domain.objects.all()

    return qs


def data_this_domain(request, slug):
    """this uses the serializer to convert the data 'Domain.objects.all()' to 'geojson' data"""
    domain = serialize(
        "geojson",
        Domain.objects.filter(slug=slug),
        geometry_field=("geom"),
    )
    return HttpResponse(domain, content_type="json")


def data_all_domains(request):
    """this uses the serializer to convert the data 'Domain.objects.all()' to 'geojson' data"""
    domain = serialize(
        "geojson",
        get_my_queryset(request),
    )
    return HttpResponse(domain, content_type="json")


@login_required
@permission_required("domains.change_domain")
def disable_all_domains(request):
    """disable all domain and return list view"""
    campaign_id = request.session.get("campaign_id", None)
    Domain.disable_all(campaign_id)
    return redirect(reverse_lazy("domains:redirect"))


@login_required
@permission_required("domains.change_domain")
def enable_all_domains(request):
    """enable all domain and return list view"""
    campaign_id = request.session.get("campaign_id", None)
    Domain.enable_all(campaign_id)
    return redirect(reverse_lazy("domains:redirect"))


@login_required
@permission_required("domains.change_domain")
def download_config(request):
    """download config files for Domain and return list view"""
    qs = get_my_queryset(request)
    domain = qs.order_by("name").first()
    domain.save()
    messages.info(request, "Domains config file successfully downloaded")
    return redirect(reverse_lazy("domains:redirect"))


class DomainDetailListView(LoginRequiredMixin, SuccessMessageMixin, ListView):
    # based on https://stackoverflow.com/a/54461397
    model = Domain
    template_name = "domains/domain_detail_list.html"
    context_object_name = "domains"
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
            form = DomainCampaignForm(data)
        else:
            form = DomainCampaignForm()

        context = super().get_context_data(**kwargs)
        domain_url = {
            "domain-add": reverse_lazy("domains:create"),
            "domain-detail": reverse_lazy("domains:detail", kwargs={"slug": "dummy"}),
            "domain-redirect": reverse_lazy("domains:redirect"),
            #     "domains:redirect", kwargs={"slug": "dummy"}
        }
        domain_data = {
            "domain-all": reverse_lazy("domains:all_domains"),
        }
        grid_data = {
            "grid-all": reverse_lazy("model_grids:all_grids"),
        }

        context["domain_url"] = domain_url
        context["domain_data"] = domain_data
        context["grid_data"] = grid_data
        context[self.detail_context_object_name] = self.object
        context["form"] = form
        return context


domain_detail_list_view = DomainDetailListView.as_view()


class DomainCampaignDetailListView(DomainDetailListView):
    def get_queryset(self):
        return get_my_queryset(self.request)
        # raise NotImplementedError('You need to provide the queryset for the object')


domain_campaign_detail_list_view = DomainCampaignDetailListView.as_view()


class DomainListView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    ListView,
):
    model = Domain
    template_name = "domains/domain_list.html"
    context_object_name = "domains"
    paginate_by = 14

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        grid_data = {
            "grid-all": reverse_lazy("model_grids:all_grids"),
        }
        domain_url = {
            "domain-add": reverse_lazy("domains:create"),
            "domain-detail": reverse_lazy("domains:detail", kwargs={"slug": "dummy"}),
            "domain-redirect": reverse_lazy("domains:redirect"),
        }
        domain_data = {
            "domain-all": reverse_lazy("domains:all_domains"),
        }

        context["grid_data"] = grid_data
        context["domain_url"] = domain_url
        context["domain_data"] = domain_data
        context["form"] = DomainForm()
        return context


domain_list_view = DomainListView.as_view()


class DomainDetailView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    DetailView,
):
    model = Domain
    context_object_name = "domain"
    slug_field = "slug"
    template_name = "domains/domain_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        grid_data = {
            "grid-all": reverse_lazy("model_grids:all_grids"),
        }
        domain_url = {
            "domain-add": reverse_lazy("domains:create"),
            "domain-detail": reverse_lazy("domains:detail", kwargs={"slug": "dummy"}),
            "domain-redirect": reverse_lazy("domains:redirect"),
        }
        domain_data = {
            "domain-local": reverse_lazy(
                "domains:this_domain", kwargs={"slug": self.object.slug}
            ),
            "domain-all": reverse_lazy("domains:all_domains"),
        }

        context["grid_data"] = grid_data
        context["domain_url"] = domain_url
        context["domain_data"] = domain_data
        context["form"] = DomainForm()

        return context


domain_detail_view = DomainDetailView.as_view()


class DomainUpdateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    SuccessMessageMixin,
    UpdateView,
):
    permission_required = "domains.change_domain"
    model = Domain
    context_object_name = "domain"
    slug_field = "slug"
    form_class = DomainUpdateForm
    success_message = _("Domain '%(name)s' successfully updated")

    def get_initial(self):
        initial = super().get_initial()
        # update initial field defaults with custom set default values:
        obj = self.object
        data = {
            "name": obj.name,
            "west": obj.west,
            "east": obj.east,
            "north": obj.north,
            "south": obj.south,
            "altitude": obj.altitude,
            "description": obj.description,
            "is_active": obj.is_active,
        }
        initial.update(data)
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        domain_data = {
            "domain-local": reverse_lazy(
                "domains:this_domain", kwargs={"slug": self.object.slug}
            ),
        }
        domain_url = {
            "domain-add": reverse_lazy("domains:create"),
            "domain-detail": reverse_lazy("domains:detail", kwargs={"slug": "dummy"}),
            "domain-redirect": reverse_lazy("domains:redirect"),
        }
        grid_data = {
            "grid-all": reverse_lazy("model_grids:all_grids"),
        }

        context["domain_data"] = domain_data
        context["domain_url"] = domain_url
        context["grid_data"] = grid_data
        return context

    def form_valid(self, form):
        # Here, add geometry using lon, lat
        # passed in form.cleaned_data['message']
        instance = form.save(commit=False)
        # capitalize name
        instance.name = form.cleaned_data.get("name").capitalize()
        west = float(form.cleaned_data.get("west", 0))
        east = float(form.cleaned_data.get("east", 0))
        north = float(form.cleaned_data.get("north", 0))
        south = float(form.cleaned_data.get("south", 0))
        alt = float(form.cleaned_data.get("altitude", 0))

        coords = (
            (west, north, alt),
            (east, north, alt),
            (east, south, alt),
            (west, south, alt),
            (west, north, alt),
        )
        instance.geom = GeoPolygon(coords)

        return super().form_valid(form)

    def get_success_url(self):
        obj = self.object
        # url = reverse_lazy("domains:detail_list", kwargs={"slug": obj.slug})
        pk = obj.active_campaign
        if pk:
            url = reverse_lazy(
                "domains:campaign_detail_list", kwargs={"pk": pk, "slug": obj.slug}
            )
        else:
            url = reverse_lazy("domains:detail_list", kwargs={"slug": obj.slug})

        return url

    def get_success_message(self, clean_data):
        messages.info(self.request, "Domains config file successfully updtaed")
        return super().get_success_message(clean_data)


domain_update_view = DomainUpdateView.as_view()


class DomainCreateView(
    PermissionRequiredMixin,
    LoginRequiredMixin,
    SuccessMessageMixin,
    CreateView,
):
    permission_required = "domains.change_domain"
    model = Domain
    form_class = DomainForm
    context_object_name = "domains"
    template_name = "domains/domain_create.html"

    success_message = _("Domain '%(name)s' successfully added")

    def get_initial(self):
        initial = super().get_initial()
        # update initial field defaults with custom set default values:
        _bbox = self.request.GET.getlist("bbox", None)
        if _bbox and _bbox is not None:
            _west, _north, _east, _south = _bbox

            try:
                _west = float(_west)
            except Exception:
                raise ValueError(f"west {_west} must be a float {type(_west)}")

            try:
                _east = float(_east)
            except Exception:
                raise ValueError(f"east {_east} must be a float {type(_east)}")

            try:
                _north = float(_north)
            except Exception:
                raise ValueError(f"north {_north} must be a float {type(_north)}")

            try:
                _south = float(_south)
            except Exception:
                raise ValueError(f"south {_south} must be a float {type(_south)}")
        else:
            _west, _east, _north, _south = None, None, None, None

        if None in [_west, _east, _north, _south]:
            _west, _east, _north, _south, _alt = None, None, None, None, None
        else:
            _alt = 0.0

        active_campaign = self.request.session.get("campaign_id", None)
        data = {
            "west": _west,
            "east": _east,
            "north": _north,
            "south": _south,
            "altitude": _alt,
            "campaigns": active_campaign,
        }
        initial.update(data)
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        domain_url = {
            "domain-add": reverse_lazy("domains:create"),
            "domain-detail": reverse_lazy("domains:detail", kwargs={"slug": "dummy"}),
            "domain-redirect": reverse_lazy("domains:redirect"),
        }
        domain_data = {
            "domain-all": reverse_lazy("domains:all_domains"),
        }
        # grid_data = {
        #     "grid-all": reverse_lazy("model_grids:all_grids"),
        # }

        context["domain_data"] = domain_data
        context["domain_url"] = domain_url
        # context["grid_data"] = grid_data
        return context

    def form_valid(self, form):
        # Here, add geometry using lon, lat
        # passed in form.cleaned_data['message']
        instance = form.save(commit=False)
        # capitalize name
        instance.name = form.cleaned_data.get("name").capitalize()
        west = float(form.cleaned_data.get("west", 0))
        east = float(form.cleaned_data.get("east", 0))
        north = float(form.cleaned_data.get("north", 0))
        south = float(form.cleaned_data.get("south", 0))
        alt = float(form.cleaned_data.get("altitude", 0))

        coords = (
            (west, north, alt),
            (east, north, alt),
            (east, south, alt),
            (west, south, alt),
            (west, north, alt),
        )
        instance.geom = GeoPolygon(coords)

        # add active campaign
        _campaign_id = self.request.session.get("campaign_id", None)
        if not _campaign_id:
            _campaign_id = None
        instance.active_campaign = _campaign_id

        return super().form_valid(form)

    def get_success_url(self):
        obj = self.object

        pk = obj.active_campaign
        if pk:
            url = reverse_lazy(
                "domains:campaign_detail_list", kwargs={"pk": pk, "slug": obj.slug}
            )
        else:
            url = reverse_lazy("domains:detail_list", kwargs={"slug": obj.slug})

        return url

    def get_success_message(self, clean_data):
        messages.info(self.request, "Domains config file successfully updated")
        return super().get_success_message(clean_data)


domain_create_view = DomainCreateView.as_view()


class DomainDeleteView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    SuccessMessageMixin,
    DeleteView,
):
    permission_required = "domains.delete_domain"
    model = Domain
    context_object_name = "domain"
    slug_field = "slug"

    success_message = _("Domain '%(name)s' successfully removed")
    success_url = reverse_lazy("domains:redirect")

    def delete(self, request, *args, **kwargs):
        """ """
        # SuccessMessageMixin hooks to form_valid
        # which is not present on DeleteView to push its message to the user.
        # see https://stackoverflow.com/questions/24822509/success-message-in-deleteview-not-shown
        obj = self.get_object()
        messages.info(self.request, "Domains config file successfully updated")
        messages.success(self.request, self.success_message % obj.__dict__)
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        domain_data = {
            "domain-local": reverse_lazy(
                "domains:this_domain", kwargs={"slug": self.object.slug}
            ),
        }
        domain_url = {
            "domain-add": reverse_lazy("domains:create"),
            "domain-detail": reverse_lazy("domains:detail", kwargs={"slug": "dummy"}),
            "domain-redirect": reverse_lazy("domains:redirect"),
        }
        grid_data = {
            "grid-all": reverse_lazy("model_grids:all_grids"),
        }

        context["domain_data"] = domain_data
        context["domain_url"] = domain_url
        context["grid_data"] = grid_data
        return context


domain_confirm_delete_view = DomainDeleteView.as_view()


class DomainRedirectView(
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
                    self.pattern_name = "domains:campaign_detail_list"
                    obj = (
                        Domain.objects.filter(campaigns=_campaign_id)
                        .order_by("name")
                        .first()
                    )
                    kwargs["slug"] = obj.slug
                except Exception:
                    self.pattern_name = "domains:create"
                else:
                    kwargs["pk"] = _campaign_id

        else:
            if not obj:
                try:
                    self.pattern_name = "domains:detail_list"
                    obj = Domain.objects.order_by("name").first()
                    kwargs["slug"] = obj.slug
                except Exception:
                    self.pattern_name = "domains:create"

        return super().get_redirect_url(*args, **kwargs)


# class DomainRedirectView(
#     LoginRequiredMixin,
#     RedirectView,
# ):
#     """redirect to plot object detail page"""
#
#     def get_redirect_url(self, slug, *args, **kwargs):
#         _domain = get_object_or_404(Domain, slug=slug)
#         # look for session variable
#         if _domain:
#             # if domain object defined
#             _type = VMType.objects.get(Q(name="op1"))
#             _location = _domain
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
#             else:
#                 self.pattern_name = "404"
#
#         # if not obj:
#
#         return super().get_redirect_url(*args, **kwargs)


domain_redirect_view = DomainRedirectView.as_view()


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
    form = DomainCampaignForm(data)
    if form.is_valid():
        data = {}
        # save location, and date
        request.session["campaign_id"] = campaign_id
        # update active campaign in database
        if campaign_id:
            Domain.active_campaign_is(campaign_id)
            Station.active_campaign_is(campaign_id)
        else:
            Domain.active_campaign_is(None)
            Station.active_campaign_is(None)

        data["url"] = reverse("domains:redirect")
        return JsonResponse(data)
    else:
        return render(request, "domains/domain_detail_list.html", {"form": form})
