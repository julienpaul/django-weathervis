# Stdlib imports
# Core Django imports
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView
from django.views.generic.edit import FormView

# Third-party app imports
# Imports from my apps
from .forms import UserUpdateForm, UserUpgradeForm

User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):

    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):

    model = User
    form_class = UserUpdateForm
    template_name = "users/user_form.html"
    success_message = _("Information successfully updated")

    def get_success_url(self):
        return self.request.user.get_absolute_url()  # type: ignore [union-attr]

    def get_object(self):
        return self.request.user


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()


class UserUpgradeFormView(LoginRequiredMixin, SuccessMessageMixin, FormView):
    template_name = "users/user_upgrade_request.html"
    form_class = UserUpgradeForm
    success_url = reverse_lazy("users:redirect")
    success_message = _(
        "Upgrade request successfully sent. You will get an answer as soon as possible."
    )

    def get_initial(self):
        initial = super(UserUpgradeFormView, self).get_initial()
        # update initial field defaults with custom set default values:
        user = self.request.user
        data = {
            "name": user.name,
            "username": user.username,
            "organisation": user.organisation,
        }
        initial.update(data)
        return initial

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        user = self.request.user
        # send request email
        form.send_email(user)
        # add information in user profile
        form.update_user(user)
        return super().form_valid(form)


user_upgrade_request_view = UserUpgradeFormView.as_view()
