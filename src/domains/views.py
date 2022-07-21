# Stdlib imports
# Core Django imports
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.gis.geos import Polygon as GeoPolygon
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
from src.vertical_meteograms.forms import VerticalMeteogramForm
from src.vertical_meteograms.models import VerticalMeteogram, VMDate, VMType

from .forms import DomainForm, DomainUpdateForm
from .models import Domain


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
        Domain.objects.all(),
    )
    return HttpResponse(domain, content_type="json")


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
            "domain-redirect": reverse_lazy(
                "domains:redirect", kwargs={"slug": "dummy"}
            ),
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
            "domain-redirect": reverse_lazy(
                "domains:redirect", kwargs={"slug": "dummy"}
            ),
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
    success_url = reverse_lazy("domains:list")

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

        data = {
            "west": _west,
            "east": _east,
            "north": _north,
            "south": _south,
            "altitude": _alt,
        }
        initial.update(data)
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        domain_url = {
            "domain-add": reverse_lazy("domains:create"),
            "domain-detail": reverse_lazy("domains:detail", kwargs={"slug": "dummy"}),
            "domain-redirect": reverse_lazy(
                "domains:redirect", kwargs={"slug": "dummy"}
            ),
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

        return super().form_valid(form)


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
    success_url = reverse_lazy("domains:list")

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
            "domain-redirect": reverse_lazy(
                "domains:redirect", kwargs={"slug": "dummy"}
            ),
        }
        grid_data = {
            "grid-all": reverse_lazy("model_grids:all_grids"),
        }

        context["domain_data"] = domain_data
        context["domain_url"] = domain_url
        context["grid_data"] = grid_data
        return context

    def delete(self, request, *args, **kwargs):
        """ """
        # SuccessMessageMixin hooks to form_valid
        # which is not present on DeleteView to push its message to the user.
        # see https://stackoverflow.com/questions/24822509/success-message-in-deleteview-not-shown
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super().delete(request, *args, **kwargs)


domain_confirm_delete_view = DomainDeleteView.as_view()


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
            "domain-redirect": reverse_lazy(
                "domains:redirect", kwargs={"slug": "dummy"}
            ),
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
        url = reverse_lazy("domains:detail", kwargs={"slug": obj.slug})

        return url


domain_update_view = DomainUpdateView.as_view()


class DomainRedirectView(
    LoginRequiredMixin,
    RedirectView,
):
    """redirect to plot object detail page"""

    def get_redirect_url(self, slug, *args, **kwargs):
        _domain = get_object_or_404(Domain, slug=slug)
        # look for session variable
        if _domain:
            # if domain object defined
            _type = VMType.objects.get(Q(name="op1"))
            _location = _domain
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
            else:
                self.pattern_name = "404"

        # if not obj:

        return super().get_redirect_url(*args, **kwargs)


domain_redirect_view = DomainRedirectView.as_view()
