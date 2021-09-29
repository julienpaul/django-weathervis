# Stdlib imports
# Core Django imports
from crispy_forms.bootstrap import Field, FieldWithButtons, StrictButton
from crispy_forms.layout import Button, ButtonHolder, Hidden, Layout, Submit
from django import forms
from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.utils.http import urlencode

# Third-party app imports
# Imports from my app
from src.utils.mixins import CrispyMixin

# TODO fix cancel button on UserUpdateForm

User = get_user_model()


class UserChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User


class UserCreationForm(admin_forms.UserCreationForm):
    class Meta(admin_forms.UserCreationForm.Meta):
        model = User
        fields = ("username", "email")


class UserUpdateForm(CrispyMixin, forms.ModelForm):
    submit_label = "Update"
    current_url = "users:update"

    class Meta:
        model = User
        fields = ["username", "name", "bio", "organisation"]

    def _init_helper_layout(self):
        """initialise crispy layout"""
        self.helper.layout = Layout(
            Hidden("next", "{{ request.GET.path }}"),
            Field("name"),
            FieldWithButtons(
                "organisation",
                StrictButton(
                    "<i class='bi bi-plus-lg'></i>",
                    css_class="btn-success",
                    onclick='window.location.href = "{}?{}";'.format(
                        reverse_lazy("organisations:list"),
                        urlencode({"next": reverse_lazy(self.current_url)}),
                    ),
                ),
            ),
            ButtonHolder(
                Submit("submit", "Submit", css_class="btn-success"),
                Button(
                    "cancel",
                    "Cancel",
                    css_class="btn-primary",
                    onclick="history.go(-1);",
                ),
            ),
        )

    def _custom_helper(self):
        """customize crispy form"""
        self.helper.help_text_as_placeholder = True
        # add some field
        self.helper.layout.insert(0, Field("username", readonly=True))
        self.helper.layout.insert(-1, Field("bio"))
        # hide help_text from username
        self.fields["username"].help_text = None


class UserUpgradeForm(UserUpdateForm):
    submit_label = "Send Request"
    current_url = "users:upgrade_request"

    motivation = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": "Please enter the  description"})
    )

    class Meta(UserUpdateForm.Meta):
        fields = ("name", "organisation", "motivation")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _custom_helper(self):
        """customize crispy form"""
        # force all fields to be required
        for key in self.fields:
            self.fields[key].required = True
            # add some field
        self.helper.layout.insert(-1, Field("motivation"))

    def clean(self):
        """
        overwrite method to check user profile parameters have not been changed.

        assume 'motivation' is the only none user elements
        """
        cleaned_data = super().clean()
        # list all attributes of UpgradePermisionForm
        attrs = list(self.fields)
        # remove 'motivation' element
        attrs.remove("motivation")
        if self.has_changed():
            for x in attrs:
                msg = f"You are not allowed to use another {x} than '{self[x].initial}'"
                if x in self.changed_data and self[x].initial:
                    # x has changed but was not empty
                    self.add_error(x, msg)

        return cleaned_data

    def update_user(self, user: User):
        """update user profile with UserUpgradeForm result"""
        attrs = list(self.fields)
        attrs.remove("motivation")
        updated_user = User.objects.get(id=user.id)
        if self.has_changed():
            for x in attrs:
                if x in self.changed_data and not self[x].initial:
                    # overwrite only empty field
                    updated_user[x] = self.cleaned_data.get(x)
            updated_user.save()

    def send_email(self, user: User):

        current_site = Site.objects.get_current()

        """send request to upgrade user permission
        to all staff members
        """
        # send email using the self.cleaned_data dictionary
        subject = "Weahtervis: request to upgrade account"
        message = f"""A user request to upgrade his permission.

        Name
            {self.cleaned_data.get('name')}
        Username
            {user.username}
        Organisation
            {self.cleaned_data.get('organisation')}
        Motivation
            {self.cleaned_data.get('motivation')}

        you could allow it from the weathervis admin page.
        { current_site.domain }/admin/users/user/{user.id}/change/"""
        staff = User.objects.filter(is_staff=True)
        recipient_list = [s.email for s in staff]

        if not recipient_list:
            # no staff members
            raise ValueError("no recipient to who send email")

        send_mail(subject, message, None, recipient_list)
