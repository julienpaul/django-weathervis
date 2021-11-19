# Stdlib imports
# Core Django imports
from django.contrib.gis import admin

# Third-party app imports
# Imports from my apps
from .models import WeatherForecastBorder

admin.site.register(WeatherForecastBorder, admin.OSMGeoAdmin)
