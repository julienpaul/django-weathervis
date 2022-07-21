# Stdlib imports
# Core Django imports
from django.contrib.gis import admin
from leaflet.admin import LeafletGeoAdmin

# Third-party app imports
# Imports from my apps
from .models import Domain


@admin.register(Domain)
class DomainAdmin(LeafletGeoAdmin):
    list_display = [
        "name",
        "geom",
    ]
