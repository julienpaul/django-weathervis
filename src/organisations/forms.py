# Stdlib imports
# Core Django imports
from crispy_forms.bootstrap import FieldWithButtons
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django import forms
from django.utils.translation import gettext_lazy as _

# Third-party app imports
# Imports from my app
from .models import Organisation


class OrganisationForm(forms.ModelForm):
    class Meta:
        model = Organisation
        fields = ["name"]
        labels = {
            "name": _("Add a new organisation"),
        }

    # TODO voir pour creer MIXINs
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
            FieldWithButtons(
                "name",
                Submit(
                    "submit",
                    "Submit",
                    css_class="btn-success",
                ),
            ),
        )

    def _custom_helper(self):
        """customize crispy form"""
        pass
