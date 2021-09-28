# Stdlib imports
# Core Django imports
from crispy_forms.bootstrap import Field, FieldWithButtons, StrictButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Button, ButtonHolder, Hidden, Layout, Submit
from django import forms
from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.utils.http import urlencode

# Third-party app imports
# Imports from my apps

User = get_user_model()


class UserChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User


class UserCreationForm(admin_forms.UserCreationForm):
    class Meta(admin_forms.UserCreationForm.Meta):
        model = User
        fields = ("username", "email")


class UserUpdateForm(forms.ModelForm):
    submit_label = "Update"
    current_url = "users:update"

    class Meta:
        model = User
        fields = ["username", "name", "bio", "organisation"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # init crispy helper
        self.helper = FormHelper()
        self._init_helper_layout()
        # customize it
        self._custom_helper()

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
