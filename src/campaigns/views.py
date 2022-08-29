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
from .forms import CampaignForm
from .models import Campaign


class CampaignListView(LoginRequiredMixin, ListView):
    model = Campaign
    context_object_name = "campaigns"
    template_name = "campaigns/campaign_list.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CampaignForm()
        return context


campaign_list_view = CampaignListView.as_view()


class CampaignUpdateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    SuccessMessageMixin,
    UpdateView,
):
    permission_required = "campaigns.change_campaign"
    model = Campaign
    form_class = CampaignForm
    context_object_name = "campaign"
    template_name = "campaigns/campaign_form.html"
    success_message = _("Campaign '%(name)s' successfully updated")

    def get_success_url(self):
        url = reverse_lazy("campaigns:list")

        return url


campaign_update_view = CampaignUpdateView.as_view()


class CampaignCreateView(
    PermissionRequiredMixin,
    LoginRequiredMixin,
    SuccessMessageMixin,
    CreateView,
):
    permission_required = "campaigns.change_campaign"
    model = Campaign
    form_class = CampaignForm
    context_object_name = "campaign"
    template_name = "campaigns/campaign_form.html"

    success_message = _("Campaign '%(name)s' successfully added")
    success_url = reverse_lazy("campaigns:list")


campaign_create_view = CampaignCreateView.as_view()


class CampaignDeleteView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    SuccessMessageMixin,
    DeleteView,
):
    permission_required = "campaigns.delete_campaign"
    model = Campaign
    # context_object_name = "campaigns"

    success_message = _("Campaign '%(name)s' successfully removed")
    success_url = reverse_lazy("campaigns:list")

    def delete(self, request, *args, **kwargs):
        """ """
        # SuccessMessageMixin hooks to form_valid
        # which is not present on DeleteView to push its message to the user.
        # see https://stackoverflow.com/questions/24822509/success-message-in-deleteview-not-shown
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super().delete(request, *args, **kwargs)


campaign_confirm_delete_view = CampaignDeleteView.as_view()
