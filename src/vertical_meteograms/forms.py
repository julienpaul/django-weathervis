# Stdlib imports
# Core Django imports
from crispy_forms.bootstrap import Field
from crispy_forms.layout import Button, ButtonHolder, Column, Layout, Row, Submit
from django import forms
from django.urls import reverse, reverse_lazy

# Third-party app imports
# Imports from my app
from src.utils.mixins import CrispyMixin

from .models import VerticalMeteogram

# see https://simpleisbetterthancomplex.com/tutorial/2016/08/29/how-to-work-with-ajax-request-with-django.html


class CustomFieldCarousel(Field):
    template = "vmeteograms/custom_carousel.html"


class VerticalMeteogramForm(CrispyMixin, forms.ModelForm):
    class Meta:
        model = VerticalMeteogram
        fields = ["location", "date"]

    def _init_helper_layout(self):
        """initialise crispy layout"""

        self.helper.attrs = {
            "data-change-plot-url": reverse_lazy("vmeteograms:change_plot"),
            # "data-select-location-url": reverse_lazy("vmeteograms:select_location"),
            # "data-select-date-url": reverse_lazy("vmeteograms:select_date"),
            "data-show-plot-url": reverse_lazy("vmeteograms:show_plot"),
        }
        self.helper.layout = Layout(
            Row(
                Column(
                    "location",
                    # css_class="form-group col-md-6 mb-0 js-change-plot",
                    # css_class="form-group col-md-6 mb-0 js-select-location",
                    css_class="form-group col-md-6 mb-0",
                    css_id="change_location_id",
                ),
                # Column("type", css_class="form-group col-md-4 mb-0 js-select-type"),
                # Column("date", css_class="form-group col-md-6 mb-0 js-select-date"),
                Column(
                    "date",
                    # css_class="form-group col-md-6 mb-0 js-change-plot",
                    css_class="form-group col-md-6 mb-0",
                    css_id="change_date_id",
                ),
                css_class="form-row",
            ),
        )


class VerticalMeteogramCreate(VerticalMeteogramForm):
    class Meta:
        model = VerticalMeteogram
        fields = ["location", "type", "date"]

    def _init_helper_layout(self):
        """initialise crispy layout"""

        self.helper.layout = Layout(
            Row(
                Column(
                    "location",
                    css_class="form-group col-md-4 mb-0",
                ),
                Column("type", css_class="form-group col-md-4 mb-0"),
                Column("date", css_class="form-group col-md-4 mb-0"),
                css_class="form-row",
            ),
            ButtonHolder(
                Submit("submit", "Submit", css_class="btn-success"),
                Button(
                    "back",
                    "Back to list",
                    css_class="btn-primary",
                    onclick="window.location.href = '{}';".format(
                        reverse("vmeteograms:list")
                    ),
                ),
            ),
        )
