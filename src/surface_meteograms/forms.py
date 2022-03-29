# Stdlib imports
# Core Django imports
from crispy_forms.layout import Button, ButtonHolder, Column, Layout, Row, Submit
from django import forms
from django.urls import reverse, reverse_lazy

# Third-party app imports
# Imports from my app
from src.utils.mixins import CrispyMixin

from .models import SurfaceMeteogram


class SurfaceMeteogramForm(CrispyMixin, forms.ModelForm):
    class Meta:
        model = SurfaceMeteogram
        fields = ["location", "points", "date"]

    def _init_helper_layout(self):
        """initialise crispy layout"""

        self.helper.attrs = {
            "data-change-plot-url": reverse_lazy("smeteograms:change_plot"),
            "data-show-plot-url": reverse_lazy("smeteograms:show_plot"),
        }
        self.helper.layout = Layout(
            Row(
                Column(
                    "location",
                    css_class="form-group col-md-4 mb-0",
                    css_id="change_location_id",
                ),
                Column(
                    "points",
                    css_class="form-group col-md-4 mb-0",
                    css_id="change_points_id",
                ),
                Column(
                    "date",
                    css_class="form-group col-md-4 mb-0",
                    css_id="change_date_id",
                ),
                css_class="form-row",
            ),
        )


class SurfaceMeteogramCreate(SurfaceMeteogramForm):
    class Meta:
        model = SurfaceMeteogram
        fields = ["location", "type", "points", "date"]

    def _init_helper_layout(self):
        """initialise crispy layout"""

        self.helper.layout = Layout(
            Row(
                Column(
                    "location",
                    css_class="form-group col-md-3 mb-0",
                ),
                Column("type", css_class="form-group col-md-3 mb-0"),
                Column("points", css_class="form-group col-md-3 mb-0"),
                Column("date", css_class="form-group col-md-3 mb-0"),
                css_class="form-row",
            ),
            ButtonHolder(
                Submit("submit", "Submit", css_class="btn-success"),
                Button(
                    "back",
                    "Back to list",
                    css_class="btn-primary",
                    onclick="window.location.href = '{}';".format(
                        reverse("smeteograms:list")
                    ),
                ),
            ),
        )
