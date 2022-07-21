# Stdlib imports
# Core Django imports
from crispy_forms.bootstrap import Field
from crispy_forms.layout import (
    HTML,
    Button,
    ButtonHolder,
    Column,
    Hidden,
    Layout,
    Row,
    Submit,
)
from django import forms

# Third-party app imports
# Imports from my apps
from src.utils.mixins import CrispyMixin
from src.utils.util import degree_sign as deg

from .models import Domain


class DomainForm(CrispyMixin, forms.ModelForm):
    current_url = "domains:create"

    # lower right corner
    east = forms.DecimalField(
        min_value=-180,
        max_value=180,
        help_text=f"{deg}E",
        max_digits=9,
        decimal_places=6,
    )
    south = forms.DecimalField(
        min_value=-90,
        max_value=90,
        help_text=f"{deg}N",
        max_digits=8,
        decimal_places=6,
    )

    # upper left corner
    west = forms.DecimalField(
        min_value=-180,
        max_value=180,
        help_text=f"{deg}E",
        max_digits=9,
        decimal_places=6,
    )
    north = forms.DecimalField(
        min_value=-90,
        max_value=90,
        help_text=f"{deg}N",
        max_digits=8,
        decimal_places=6,
    )

    altitude = forms.DecimalField(
        min_value=0,
        help_text="m",
        max_digits=11,
        decimal_places=6,
    )

    class Meta:
        model = Domain
        fields = [
            "name",
            "is_active",
            "description",
        ]

    def _init_helper_layout(self):
        """initialise crispy layout"""
        self.helper.error_text_inline = True
        self.helper.layout = Layout(
            Hidden("next", "{{ request.GET.path }}"),
            Row(
                Column(
                    Field("name"),
                    css_class="form-group col-md-4 mb-0",
                ),
                css_class="form-row",
            ),
            HTML("<legend>Boundary Box Coordinates</legend>"),
            Row(
                Column(
                    css_class="form-group col-md-4 my-0 mx-0",
                ),
                Column(
                    Field("north"),
                    css_class="form-group col-md-4 my-0 mx-0",
                ),
                Column(
                    css_class="form-group col-md-4 my-0  mx-0",
                ),
                css_class="form-row",
            ),
            Row(
                Column(
                    Field("west"),
                    css_class="form-group col-md-4 my-0  mx-0",
                ),
                Column(
                    css_class="form-group col-md-4 my-0  mx-0",
                ),
                Column(
                    Field("east"),
                    css_class="form-group col-md-4 my-0  mx-0",
                ),
                css_class="form-row",
            ),
            Row(
                Column(
                    css_class="form-group col-md-4 my-0  mx-0",
                ),
                Column(
                    Field("south"),
                    css_class="form-group col-md-4 my-0  mx-0",
                ),
                Column(
                    css_class="form-group col-md-4 my-0  mx-0",
                ),
                css_class="form-row",
            ),
            Row(
                Column(
                    Field("altitude"),
                    css_class="form-group col-md-4 mb-0",
                ),
                css_class="form-row",
            ),
            # Field("name"),
            # Fieldset("Coordinates", "latitude", "longitude", "altitude"),
            Field("is_active"),
            Field("description"),
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


class DomainUpdateForm(DomainForm):
    def _custom_helper(self):
        """customize crispy form"""
        # change some field
        self.fields["name"].disabled = True
