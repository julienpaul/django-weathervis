# Stdlib imports
import random

# Core Django imports
# Third-party app imports
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    RedirectView,
    UpdateView,
)

# Imports from my apps
from src.stations.models import Station
from src.vertical_meteograms.models import VMDate

from .forms import SurfaceMeteogramCreate, SurfaceMeteogramForm
from .models import SMPoints, SMType, SurfaceMeteogram


class SurfaceMeteogramDetailView(LoginRequiredMixin, SuccessMessageMixin, DetailView):
    model = SurfaceMeteogram
    context_object_name = "smeteogram"
    template_name = "smeteograms/smeteogram_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = SurfaceMeteogramForm()
        return context


smeteogram_detail_view = SurfaceMeteogramDetailView.as_view()


class SurfaceMeteogramRedirectView(RedirectView):
    """redirect to create either one random object detail page"""

    def get_redirect_url(self, *args, **kwargs):
        objects = SurfaceMeteogram.objects.all()
        if len(objects) == 0:
            self.pattern_name = "smeteograms:create"
        else:
            obj = random.choice(objects)
            self.pattern_name = "smeteograms:detail"
            kwargs["slug"] = obj.slug
        return super().get_redirect_url(*args, **kwargs)


smeteogram_redirect_view = SurfaceMeteogramRedirectView.as_view()


class SurfaceMeteogramUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = SurfaceMeteogram
    context_object_name = "smeteogram"
    template_name = "smeteograms/smeteogram_detail.html"
    form_class = SurfaceMeteogramForm
    success_message = _("Surface Meteogram successfully updated")

    def get_initial(self):
        initial = super().get_initial()
        # update initial field defaults with custom set default values:
        obj = self.object
        data = {
            "type": obj.type,
            "location": obj.location,
            "points": obj.points,
            "date": obj.date,
        }
        initial.update(data)
        return initial

    def get_success_url(self):
        obj = self.object
        url = reverse_lazy("smeteograms:detail", kwargs={"slug": obj.slug})

        return url


smeteogram_update_view = SurfaceMeteogramUpdateView.as_view()


class SurfaceMeteogramCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = SurfaceMeteogram
    form_class = SurfaceMeteogramCreate
    context_object_name = "smeteograms"
    template_name = "smeteograms/smeteogram_form.html"

    success_message = _("Surface Meteogram successfully added")

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form,
        with object list and error message.
        """
        self.object = self.get_queryset()
        for field in form:
            for error in field.errors:
                messages.add_message(self.request, messages.ERROR, error)
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        obj = self.object
        url = reverse_lazy("smeteograms:detail", kwargs={"slug": obj.slug})

        return url


smeteogram_create_view = SurfaceMeteogramCreateView.as_view()


class SurfaceMeteogramListView(LoginRequiredMixin, SuccessMessageMixin, ListView):
    model = SurfaceMeteogram
    template_name = "smeteograms/smeteogram_list.html"
    context_object_name = "smeteograms"
    paginate_by = 10


smeteogram_list_view = SurfaceMeteogramListView.as_view()


def change_plot(request):
    """ """
    _type = SMType.objects.get(Q(name="op1"))

    _location = None
    try:
        _id = request.GET.get("location", None)
        if _id:
            _location = Station.objects.get(pk=_id)
    except Station.DoesNotExist:
        pass

    _points = None
    try:
        _id = request.GET.get("points", None)
        if _id:
            _points = SMPoints.objects.get(pk=_id)
    except SMPoints.DoesNotExist:
        pass

    _date = None
    try:
        _id = request.GET.get("date", None)
        if _id:
            _date = VMDate.objects.get(pk=_id)
    except VMDate.DoesNotExist:
        pass

    data = {"type": _type, "location": _location, "points": _points, "date": _date}
    form = SurfaceMeteogramForm(data)
    if form.is_valid():
        data = {}
        smeteogram, created = SurfaceMeteogram.objects.get_or_create(
            type=_type,
            location=_location,
            points=_points,
            date=_date,
        )
        # print(f"form valid {form}")
        print(f"smeteogram {smeteogram.slug}")
        data = {
            "is_valid": True,
        }
        if data["is_valid"]:
            data["error_message"] = "this date already exists."
        data["url"] = reverse("smeteograms:detail", kwargs={"slug": smeteogram.slug})
        return JsonResponse(data)
    else:
        data = {"is_valid": False, "error_message": "this form is invalid."}
        return render(request, "smeteograms/smeteogram_detail.html", {"form": form})


def show_plot(request):
    """ """
    try:
        _type = SMType.objects.get(Q(name="op1"))
        _type_rev = SMType.objects.get(~Q(name="op1"))
    except SMType.DoesNotExist:
        _type = None

    _location = None
    try:
        location_id = request.GET.get("location", None)
        if location_id:
            _location = Station.objects.get(pk=location_id)
    except Station.DoesNotExist:
        pass

    _points = None
    try:
        _id = request.GET.get("points", None)
        if _id:
            _points = SMPoints.objects.get(pk=_id)
    except SMPoints.DoesNotExist:
        pass

    _date = None
    try:
        date_id = request.GET.get("date", None)
        if date_id:
            _date = VMDate.objects.get(pk=date_id)
    except VMDate.DoesNotExist:
        pass

    data = {"type": _type, "location": _location, "points": _points, "date": _date}
    form = SurfaceMeteogramForm(data)
    if form.is_valid():
        data = {}
        smeteogram, created = SurfaceMeteogram.objects.get_or_create(
            type=_type,
            location=_location,
            points=_points,
            date=_date,
        )
        data["img1"] = {
            "url": smeteogram.img.url,
            "nam": smeteogram.img.name,
            # "ttl": f"{smeteogram.location} {smeteogram.date.date.strftime('%Y-%m-%d %H:%M')}",
        }
        print(f"img {data['img1']}")
        smeteogram, created = SurfaceMeteogram.objects.get_or_create(
            type=_type_rev,
            location=_location,
            points=_points,
            date=_date,
        )
        data["img2"] = {
            "url": smeteogram.img.url,
            "nam": smeteogram.img.name,
            # "ttl": f"{smeteogram.location} {smeteogram.date.date.strftime('%Y-%m-%d %H:%M')}",
        }
        return JsonResponse(data)
    else:
        return render(request, "smeteograms/smeteogram_detail.html", {"form": form})
