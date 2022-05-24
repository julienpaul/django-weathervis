# Stdlib imports
# Core Django imports
from crispy_forms.bootstrap import Field
from crispy_forms.layout import Button, ButtonHolder, Column, Layout, Row, Submit
from django import forms
from django.forms import HiddenInput
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
        fields = ["location", "date", "subtext"]

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
                    css_class="form-group col-md-6 mb-0",
                    css_id="change_location_id",
                ),
                Column(
                    "date",
                    css_class="form-group col-md-6 mb-0",
                    css_id="change_date_id",
                ),
                css_class="form-row",
            ),
        )

    def _custom_helper(self):
        """customize crispy form

        rename field Date to Base Date
        """
        self.fields["date"].label = "Base Date"


class VerticalMeteogramUpdateSubtextForm(VerticalMeteogramForm):
    def _custom_helper(self):
        """customize crispy form"""
        super()._custom_helper()
        # change some field
        self.fields["location"].widget = HiddenInput()
        self.fields["date"].widget = HiddenInput()
        # self.fields["location"].disabled = True
        # self.fields["date"].disabled = True
        # add some field and buttons
        _btn = ButtonHolder(
            Submit("submit", "Submit", css_class="btn-success"),
            Button(
                "cancel",
                "Cancel",
                css_class="btn-primary",
                onclick="history.go(-1);",
            ),
        )
        self.helper.layout.insert(1, _btn)
        _fld = Field("subtext")
        self.helper.layout.insert(1, _fld)
        self.fields["subtext"].label = "Change Subtext"


class VerticalMeteogramCreate(VerticalMeteogramForm):
    class Meta:
        model = VerticalMeteogram
        fields = ["location", "type", "date", "subtext"]

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
