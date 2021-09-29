# Stdlib imports
# Core Django imports
from crispy_forms.bootstrap import FieldWithButtons
from crispy_forms.layout import Layout, Submit
from django import forms
from django.utils.translation import gettext_lazy as _

# Third-party app imports
# Imports from my app
from src.utils.mixins import CrispyMixin

from .models import Organisation


class OrganisationForm(CrispyMixin, forms.ModelForm):
    class Meta:
        model = Organisation
        fields = ["name"]
        labels = {
            "name": _("Add a new organisation"),
        }

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
