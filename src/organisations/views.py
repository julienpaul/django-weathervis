# Stdlib imports
# Core Django imports
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import resolve_url
from django.urls import reverse_lazy
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import CreateView, DeleteView, ListView

# Third-party app imports
# Imports from my apps
from src.utils.mixins import SuccessURLAllowedHostsMixin

from .forms import OrganisationForm
from .models import Organisation

# TODO: add PermissionMixin so only staff member could delete organisation.
# TODO: add change view
# TODO: what if delete organisation associated to a user
# TODO: see alphabetic pagination for list organisation
#  https://djangosnippets.org/snippets/1364/
#  https://djangosnippets.org/snippets/2732/
#       see numeric pagination
#  https://augusto.to/django-pagination/
#  https://simpleisbetterthancomplex.com/tutorial/2016/08/03/how-to-paginate-with-django.html


class OrganisationView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        view = OrganisationListView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = OrganisationCreateView.as_view()
        return view(request, *args, **kwargs)


organisation_view = OrganisationView.as_view()


class OrganisationListView(ListView):
    model = Organisation
    context_object_name = "organisations"
    template_name = "organisations/organisation_list.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = OrganisationForm()
        return context


class OrganisationCreateView(
    SuccessMessageMixin, SuccessURLAllowedHostsMixin, CreateView
):
    model = Organisation
    context_object_name = "organisations"
    template_name = "organisations/organisation_list.html"
    form_class = OrganisationForm

    success_message = _("Organisation '%(name)s' successfully added")
    success_url = reverse_lazy("organisations:list")

    next_page = success_url
    redirect_field_name = "next"

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
        """Return the URL to redirect to after processing a valid form."""
        next_page = self.get_next_page()
        if next_page:
            # Redirect to this page until the session has been cleared.
            return next_page
        return super().get_success_url()

    def get_next_page(self):
        if self.next_page is not None:
            next_page = resolve_url(self.next_page)
        else:
            next_page = self.next_page

        if (
            self.redirect_field_name in self.request.POST
            or self.redirect_field_name in self.request.GET
        ):
            next_page = self.request.POST.get(
                self.redirect_field_name, self.request.GET.get(self.redirect_field_name)
            )
            url_is_safe = url_has_allowed_host_and_scheme(
                url=next_page,
                allowed_hosts=self.get_success_url_allowed_hosts(),
                require_https=self.request.is_secure(),
            )
            # Security check -- Ensure the user-originating redirection URL is
            # safe.
            if not url_is_safe:
                next_page = self.request.path
        return next_page


class OrganisationDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Organisation
    # context_object_name = "organisations"

    success_message = _("Organisation '%(name)s' successfully removed")
    success_url = reverse_lazy("organisations:list")

    def delete(self, request, *args, **kwargs):
        """ """
        # SuccessMessageMixin hooks to form_valid
        # which is not present on DeleteView to push its message to the user.
        # see https://stackoverflow.com/questions/24822509/success-message-in-deleteview-not-shown
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super().delete(request, *args, **kwargs)


organisation_confirm_delete_view = OrganisationDeleteView.as_view()
