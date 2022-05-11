# Stdlib imports
# Core Django imports
from django.contrib.gis import admin
from leaflet.admin import LeafletGeoAdmin

# Third-party app imports
# Imports from my apps
from .models import Station

# admin.site.register(Station, admin.OSMGeoAdmin)


@admin.register(Station)
class StationAdmin(LeafletGeoAdmin):
    list_display = [
        "name",
        "geom",
    ]
