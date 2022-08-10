# Stdlib imports
# Core Django imports
from crispy_forms.bootstrap import Field, FieldWithButtons, StrictButton
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
from django.contrib.gis.geos import Point as geoPoint
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from django.utils.http import urlencode

# Third-party app imports
# Imports from my apps
from src.model_grids.models import ModelGrid
from src.plots.models import StationsPlot
from src.utils.mixins import CrispyMixin
from src.utils.util import degree_sign as deg

from .models import Station


class StationForm(CrispyMixin, forms.ModelForm):
    current_url = "stations:create"

    longitude = forms.DecimalField(
        min_value=-180,
        max_value=180,
        help_text=f"{deg}E",
        max_digits=9,
        decimal_places=6,
    )
    latitude = forms.DecimalField(
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

    plots = forms.ModelMultipleChoiceField(
        required=False,
        queryset=StationsPlot.objects.all(),
        widget=forms.CheckboxSelectMultiple(
            attrs={"class": "form-check", "style": "list-style:none;"}
        ),
    )

    start_datetime = forms.DateTimeField(
        widget=forms.widgets.DateTimeInput(attrs={"placeholder": "YYYY-MM-DD HH:MM"})
    )
    end_datetime = forms.DateTimeField(
        widget=forms.widgets.DateTimeInput(attrs={"placeholder": "YYYY-MM-DD HH:MM"})
    )

    class Meta:
        model = Station
        fields = [
            "name",
            "longitude",
            "latitude",
            "altitude",
            "is_active",
            "station_id",
            "wmo_id",
            "description",
            "margin",
            "plots",
            "uses_flexpart",
            "start_datetime",
            "end_datetime",
            "alt_lower",
            "alt_upper",
            "alt_unit",
            "numb_part",
            "xmass",
            "number_grid",
        ]

    def _init_helper_layout(self):
        """initialise crispy layout"""
        self.helper.error_text_inline = False
        self.helper.layout = Layout(
            Hidden("next", "{{ request.GET.path }}"),
            Row(
                Column(
                    Field("name"),
                    css_class="form-group col-md-4 mb-0",
                ),
                Column(
                    Field("station_id"),
                    css_class="form-group col-md-4 mb-0",
                ),
                Column(
                    Field("wmo_id"),
                    css_class="form-group col-md-4 mb-0",
                ),
                css_class="form-row",
            ),
            HTML("<legend>Coordinates</legend>"),
            Row(
                Column(
                    Field("latitude"),
                    css_class="form-group col-md-4 mb-0",
                ),
                Column(
                    Field("longitude"),
                    css_class="form-group col-md-4 mb-0",
                ),
                Column(
                    Field("altitude"),
                    css_class="form-group col-md-4 mb-0",
                ),
                css_class="form-row",
            ),
            # Field("name"),
            # Fieldset("Coordinates", "latitude", "longitude", "altitude"),
            FieldWithButtons(
                "margin",
                StrictButton(
                    "<i class='bi bi-plus-lg'></i>",
                    css_class="btn-success",
                    onclick='window.location.href = "{}?{}";'.format(
                        reverse_lazy("margins:list"),
                        urlencode({"next": reverse_lazy(self.current_url)}),
                    ),
                ),
            ),
            Field("is_active"),
            Field("uses_flexpart"),
            Field("description", rows="4"),
            HTML("<div id=plots>"),
            HTML("<hr>"),
            Field("plots"),
            HTML("</div>"),
            HTML("<div id=flexpart>"),
            HTML("<hr>"),
            Row(
                Column(
                    Field("start_datetime"),
                    css_class="form-group col-md-6 mb-0",
                ),
                Column(
                    Field("end_datetime"),
                    css_class="form-group col-md-6 mb-0",
                ),
                css_class="form-row",
            ),
            Row(
                Column(
                    Field("alt_lower"),
                    css_class="form-group col-md-4 mb-0",
                ),
                Column(
                    Field("alt_upper"),
                    css_class="form-group col-md-4 mb-0",
                ),
                Column(
                    Field("alt_unit"),
                    css_class="form-group col-md-4 mb-0",
                ),
                css_class="form-row",
            ),
            Row(
                Column(
                    Field("numb_part"),
                    css_class="form-group col-md-4 mb-0",
                ),
                Column(
                    Field("xmass"),
                    css_class="form-group col-md-4 mb-0",
                ),
                Column(
                    Field("number_grid"),
                    css_class="form-group col-md-4 mb-0",
                ),
                css_class="form-row",
            ),
            HTML("</div>"),
            # HTML("&zwnj;"),
            HTML("<hr>"),
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
        # Sort plots alphabetically
        self.fields["plots"].label = "Available plots"
        self.fields["plots"].queryset = StationsPlot.objects.order_by("name")
        # rename label
        self.fields["start_datetime"].label = "Starting date"
        self.fields["end_datetime"].label = "Ending date"
        self.fields["alt_lower"].label = "Lower altitude"
        self.fields["alt_upper"].label = "Upper altitude"
        self.fields["alt_unit"].label = "Unit"
        self.fields["numb_part"].label = "Nb particles"
        self.fields["xmass"].label = "Total mass"
        # fields not required
        self.fields["start_datetime"].required = False
        self.fields["end_datetime"].required = False
        self.fields["alt_lower"].required = False
        self.fields["alt_upper"].required = False
        self.fields["alt_unit"].required = False
        self.fields["numb_part"].required = False
        self.fields["xmass"].required = False
        self.fields["number_grid"].required = False

    def clean(self):
        """check station is located inside one the registered forecast"""
        cleaned_data = super().clean()
        # capitalize name
        name = cleaned_data.get("name")
        lat = float(cleaned_data.get("latitude", 0))
        lon = float(cleaned_data.get("longitude", 0))
        alt = float(cleaned_data.get("altitude", 0))
        point = geoPoint(lon, lat, alt)

        model_grids = ModelGrid.objects.all()

        if len(model_grids) == 0:
            raise ValidationError(
                "No Weather Forecast registered. You must have registered at least one before assigning station"
            )

        for model_grid in model_grids:
            poly = model_grid.geom
            # valid = poly.contains(point)
            # valid = poly.covers(point)
            valid = point.intersects(poly)
            if valid:
                print(f"Station {name} is in {model_grid.name}")
                break

        if not valid:
            raise ValidationError(
                "Station is not inside any ModelGrid registered.",
            )

        uses_flexpart = cleaned_data.get("uses_flexpart")

        alt_lower = cleaned_data.get("alt_lower")
        alt_upper = cleaned_data.get("alt_upper")

        if uses_flexpart:
            if not alt_lower and alt_lower != 0:
                raise ValidationError("Lower altitude is a required field.")
            if not alt_upper and alt_upper != 0:
                raise ValidationError("Upper altitude is a required field.")
            if alt_upper < alt_lower:
                raise ValidationError(
                    "Flexpart release altitudes aren't sorted in ascending order.",
                )

        start_datetime = cleaned_data.get("start_datetime")
        end_datetime = cleaned_data.get("end_datetime")

        if uses_flexpart:
            if not start_datetime:
                raise ValidationError("Starting date is a required field.")
            if not end_datetime:
                raise ValidationError("Ending date is a required field.")
            if end_datetime < start_datetime:
                raise ValidationError(
                    "Flexpart release dates aren't sorted in ascending order.",
                )

        numb_part = cleaned_data.get("numb_part")
        if not isinstance(numb_part, int):
            raise ValidationError(
                "Flexpart number of particles must be an integer.",
            )

        xmass = cleaned_data.get("xmass")
        if not isinstance(xmass, int):
            raise ValidationError(
                "Flexpart xmass must be an integer.",
            )

        number_grid = cleaned_data.get("number_grid")
        if not isinstance(number_grid, int):
            raise ValidationError(
                "Flexpart number_grid must be an integer.",
            )


class StationUpdateForm(StationForm):
    def _custom_helper(self):
        """customize crispy form"""
        super()._custom_helper()
        # change some field
        self.fields["name"].disabled = True
