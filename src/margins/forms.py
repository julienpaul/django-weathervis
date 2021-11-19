# Stdlib imports
# Core Django imports
from crispy_forms.layout import HTML, Button, ButtonHolder, Fieldset, Layout, Submit
from django import forms

# Third-party app imports
# Imports from my apps
from src.utils.mixins import CrispyMixin
from src.utils.util import degree_sign as deg

from .models import Margin


class MarginForm(CrispyMixin, forms.ModelForm):
    west = forms.DecimalField(
        min_value=0,
        max_value=180,
        help_text=f"Westward offest [{deg}] from station",
        max_digits=9,
        decimal_places=6,
    )
    east = forms.DecimalField(
        min_value=0,
        max_value=180,
        help_text=f"Eastward offest [{deg}] from station",
        max_digits=9,
        decimal_places=6,
    )
    north = forms.DecimalField(
        min_value=0,
        max_value=90,
        help_text=f"Northward offest [{deg}] from station",
        max_digits=9,
        decimal_places=6,
    )
    south = forms.DecimalField(
        min_value=0,
        max_value=90,
        help_text=f"Southward offest [{deg}] from station",
        max_digits=9,
        decimal_places=6,
    )

    class Meta:
        model = Margin
        fields = [
            "east",
            "west",
            "north",
            "south",
        ]

    def _init_helper_layout(self):
        """initialise crispy layout"""
        self.helper.error_text_inline = False
        self.helper.layout = Layout(
            Fieldset("Margin offsets", "east", "west", "north", "south"),
            HTML("&zwnj;"),
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
