# Stdlib imports
# Core Django imports
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

# Third-party app imports
# Imports from my apps
from .forms import DomainsPlotForm, StationsPlotForm
from .models import DomainsPlot, StationsPlot


# ------------- Station Views -------------
class StationsPlotListView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    ListView,
):
    model = StationsPlot
    template_name = "plots/stations/stations_plot_list.html"
    context_object_name = "stations_plots"


stations_plot_list_view = StationsPlotListView.as_view()


class StationsPlotUpdateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    SuccessMessageMixin,
    UpdateView,
):
    permission_required = "plots.change_stationsplot"
    model = StationsPlot
    form_class = StationsPlotForm
    context_object_name = "stations_plot"
    template_name = "plots/stations/stations_plot_form.html"
    success_message = _("Stations Plot '%(name)s' successfully updated")

    def get_success_url(self):
        url = reverse_lazy("plots:stations_list")

        return url


stations_plot_update_view = StationsPlotUpdateView.as_view()


class StationsPlotCreateView(
    PermissionRequiredMixin,
    LoginRequiredMixin,
    SuccessMessageMixin,
    CreateView,
):
    permission_required = "plots.change_stationsplot"
    model = StationsPlot
    form_class = StationsPlotForm
    context_object_name = "stations_plots"
    template_name = "plots/stations/stations_plot_form.html"

    success_message = _("Stations Plot '%(name)s' successfully added")
    success_url = reverse_lazy("plots:stations_list")


stations_plot_create_view = StationsPlotCreateView.as_view()


class StationsPlotDeleteView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    SuccessMessageMixin,
    DeleteView,
):
    permission_required = "plots.delete_stationsplot"
    model = StationsPlot
    context_object_name = "stations_plot"
    template_name = "plots/stations/stations_plot_confirm_delete.html"

    success_message = _("Stations Plot '%(name)s' successfully removed")
    success_url = reverse_lazy("plots:stations_list")

    def delete(self, request, *args, **kwargs):
        """ """
        # SuccessMessageMixin hooks to form_valid
        # which is not present on DeleteView to push its message to the user.
        # see https://stackoverflow.com/questions/24822509/success-message-in-deleteview-not-shown
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super().delete(request, *args, **kwargs)


stations_plot_confirm_delete_view = StationsPlotDeleteView.as_view()


# ------------- Domain Views -------------
class DomainsPlotListView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    ListView,
):
    model = DomainsPlot
    template_name = "plots/domains/domains_plot_list.html"
    context_object_name = "domains_plots"


domains_plot_list_view = DomainsPlotListView.as_view()


class DomainsPlotUpdateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    SuccessMessageMixin,
    UpdateView,
):
    permission_required = "plots.change_domainsplot"
    model = DomainsPlot
    form_class = DomainsPlotForm
    context_object_name = "domains_plot"
    template_name = "plots/domains/domains_plot_form.html"
    success_message = _("Domains Plot '%(name)s' successfully updated")

    def get_success_url(self):
        url = reverse_lazy("plots:domains_list")

        return url


domains_plot_update_view = DomainsPlotUpdateView.as_view()


class DomainsPlotCreateView(
    PermissionRequiredMixin,
    LoginRequiredMixin,
    SuccessMessageMixin,
    CreateView,
):
    permission_required = "plots.change_domainsplot"
    model = DomainsPlot
    form_class = DomainsPlotForm
    context_object_name = "domains_plots"
    template_name = "plots/domains/domains_plot_form.html"

    success_message = _("Domains Plot '%(name)s' successfully added")
    success_url = reverse_lazy("plots:domains_list")


domains_plot_create_view = DomainsPlotCreateView.as_view()


class DomainsPlotDeleteView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    SuccessMessageMixin,
    DeleteView,
):
    permission_required = "plots.delete_domainsplot"
    model = DomainsPlot
    context_object_name = "domains_plot"
    template_name = "plots/domains/domains_plot_confirm_delete.html"

    success_message = _("Domains Plot '%(name)s' successfully removed")
    success_url = reverse_lazy("plots:domains_list")

    def delete(self, request, *args, **kwargs):
        """ """
        # SuccessMessageMixin hooks to form_valid
        # which is not present on DeleteView to push its message to the user.
        # see https://stackoverflow.com/questions/24822509/success-message-in-deleteview-not-shown
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super().delete(request, *args, **kwargs)


domains_plot_confirm_delete_view = DomainsPlotDeleteView.as_view()
