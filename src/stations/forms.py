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
