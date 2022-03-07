# Stdlib imports
# Core Django imports
from django.contrib.gis import admin

# Third-party app imports
# Imports from my apps
from .models import ModelGrid, ModelVariable

admin.site.register(ModelGrid, admin.OSMGeoAdmin)
admin.site.register(ModelVariable)
