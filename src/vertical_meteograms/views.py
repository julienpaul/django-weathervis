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

from .forms import VerticalMeteogramCreate, VerticalMeteogramForm
from .models import VerticalMeteogram, VMDate, VMType


class VerticalMeteogramDetailView(LoginRequiredMixin, SuccessMessageMixin, DetailView):
    model = VerticalMeteogram
    context_object_name = "vmeteogram"
    template_name = "vmeteograms/vmeteogram_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = VerticalMeteogramForm()
        return context


vmeteogram_detail_view = VerticalMeteogramDetailView.as_view()


class VerticalMeteogramRedirectView(RedirectView):
    """redirect to create either one random object detail page"""

    def get_redirect_url(self, *args, **kwargs):
        obj = None
        # look for session variable
        _location_id = self.request.session.get("location_id", None)
        _date_id = self.request.session.get("date_id", None)
        if _location_id and _date_id:
            # if session variable defined
            _type = VMType.objects.get(Q(name="op1"))
            _location = Station.objects.get(pk=_location_id)
            _date = VMDate.objects.get(pk=_date_id)
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

        if not obj:
            objects = VerticalMeteogram.objects.all()
            if len(objects) == 0:
                self.pattern_name = "vmeteograms:create"
            else:
                obj = random.choice(objects)
                self.pattern_name = "vmeteograms:detail"
                kwargs["slug"] = obj.slug

        return super().get_redirect_url(*args, **kwargs)


vmeteogram_redirect_view = VerticalMeteogramRedirectView.as_view()


class VerticalMeteogramUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = VerticalMeteogram
    context_object_name = "vmeteogram"
    template_name = "vmeteograms/vmeteogram_detail.html"
    form_class = VerticalMeteogramForm
    success_message = _("Vertical Meteogram successfully updated")

    def get_initial(self):
        initial = super().get_initial()
        # update initial field defaults with custom set default values:
        obj = self.object
        data = {
            "type": obj.type,
            "location": obj.location,
            "date": obj.date,
        }
        initial.update(data)
        return initial

    def get_success_url(self):
        obj = self.object
        url = reverse_lazy("vmeteograms:detail", kwargs={"slug": obj.slug})

        return url


vmeteogram_update_view = VerticalMeteogramUpdateView.as_view()


class VerticalMeteogramCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = VerticalMeteogram
    form_class = VerticalMeteogramCreate
    context_object_name = "vmeteograms"
    template_name = "vmeteograms/vmeteogram_form.html"

    success_message = _("Vertical Meteogram successfully added")

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
        url = reverse_lazy("vmeteograms:detail", kwargs={"slug": obj.slug})

        return url


vmeteogram_create_view = VerticalMeteogramCreateView.as_view()


class VerticalMeteogramListView(LoginRequiredMixin, SuccessMessageMixin, ListView):
    model = VerticalMeteogram
    template_name = "vmeteograms/vmeteogram_list.html"
    context_object_name = "vmeteograms"
    paginate_by = 10


vmeteogram_list_view = VerticalMeteogramListView.as_view()


def change_plot(request):
    """ """
    _type = VMType.objects.get(Q(name="op1"))

    _location = None
    try:
        _id = request.GET.get("location", None)
        if _id:
            _location = Station.objects.get(pk=_id)
    except Station.DoesNotExist:
        pass

    _date = None
    try:
        _id = request.GET.get("date", None)
        if _id:
            _date = VMDate.objects.get(pk=_id)
    except VMDate.DoesNotExist:
        pass

    data = {"type": _type, "location": _location, "date": _date}
    form = VerticalMeteogramForm(data)
    if form.is_valid():
        data = {}
        vmeteogram, created = VerticalMeteogram.objects.get_or_create(
            type=_type,
            location=_location,
            date=_date,
        )
        # print(f"form valid {form}")
        print(f"vmeteogram {vmeteogram.slug}")
        data = {
            "is_valid": True,
        }
        if data["is_valid"]:
            data["error_message"] = "this date already exists."
        data["url"] = reverse("vmeteograms:detail", kwargs={"slug": vmeteogram.slug})
        return JsonResponse(data)
    else:
        data = {"is_valid": False, "error_message": "this form is invalid."}
        return render(request, "vmeteograms/vmeteogram_detail.html", {"form": form})


# def select_location(request):
#     _id = request.GET.get("location", None)
#     print(f"location {_id}")
#     try:
#         inst = Station.objects.get(pk=_id)
#         exist = True
#     except Station.DoesNotExist:
#         exist = False
#     data = {
#         "is_taken": not exist,
#     }
#     if data["is_taken"]:
#         data["error_message"] = f"this location ({inst}) already exists."
#     return JsonResponse(data)
#
#
# def select_date(request):
#     _id = request.GET.get("date", None)
#     print(f"date_id {_id}")
#     try:
#         inst = VMDate.objects.get(pk=_id)
#         exist = True
#     except VMDate.DoesNotExist:
#         exist = False
#     data = {
#         "is_taken": not exist,
#     }
#     if data["is_taken"]:
#         data["error_message"] = f"this date ({inst}) already exists."
#     return JsonResponse(data)
#
#
# def select_type(request):
#     _id = request.GET.get("type", None)
#     print(f"type_id {_id}")
#     try:
#         inst = VMType.objects.get(pk=_id)
#         exist = True
#     except VMType.DoesNotExist:
#         exist = False
#     data = {
#         "is_taken": not exist,
#     }
#     if data["is_taken"]:
#         data["error_message"] = f"this type ({inst}) already exists."
#     return JsonResponse(data)


def show_plot(request):
    """ """
    try:
        _type = VMType.objects.get(Q(name="op1"))
        _type_rev = VMType.objects.get(~Q(name="op1"))
    except VMType.DoesNotExist:
        _type = None

    _location = None
    try:
        location_id = request.GET.get("location", None)
        if location_id:
            _location = Station.objects.get(pk=location_id)
    except Station.DoesNotExist:
        pass

    _date = None
    try:
        date_id = request.GET.get("date", None)
        if date_id:
            _date = VMDate.objects.get(pk=date_id)
    except VMDate.DoesNotExist:
        pass

    data = {"type": _type, "location": _location, "date": _date}
    form = VerticalMeteogramForm(data)
    if form.is_valid():
        data = {}
        # save location, and date
        request.session["location_id"] = _location.pk
        request.session["date_id"] = _date.pk

        vmeteogram, created = VerticalMeteogram.objects.get_or_create(
            type=_type,
            location=_location,
            date=_date,
        )
        data["img1"] = {
            "url": vmeteogram.img.url,
            "nam": vmeteogram.img.name,
            # "ttl": f"{vmeteogram.location} {vmeteogram.date.date.strftime('%Y-%m-%d %H:%M')}",
        }
        vmeteogram, created = VerticalMeteogram.objects.get_or_create(
            type=_type_rev,
            location=_location,
            date=_date,
        )
        data["img2"] = {
            "url": vmeteogram.img.url,
            "nam": vmeteogram.img.name,
            # "ttl": f"{vmeteogram.location} {vmeteogram.date.date.strftime('%Y-%m-%d %H:%M')}",
        }
        return JsonResponse(data)
    else:
        return render(request, "vmeteograms/vmeteogram_detail.html", {"form": form})
