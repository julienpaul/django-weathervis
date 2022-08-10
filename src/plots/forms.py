# Stdlib imports
# Core Django imports
from crispy_forms.bootstrap import Field
from crispy_forms.layout import HTML, Button, ButtonHolder, Layout, Submit
from django import forms

# Third-party app imports
# Imports from my apps
from src.utils.mixins import CrispyMixin

from .models import StationsPlot


class CustomMMCF(forms.ModelMultipleChoiceField):
    def label_from_instance(self, plot):
        return plot.name


class StationsPlotForm(CrispyMixin, forms.ModelForm):
    class Meta:
        model = StationsPlot
        fields = ["name", "command", "options", "description"]

    def _init_helper_layout(self):
        """initialise crispy layout"""
        self.helper.error_text_inline = False
        self.helper.layout = Layout(
            Field("name"),
            Field("command"),
            Field("options"),
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
