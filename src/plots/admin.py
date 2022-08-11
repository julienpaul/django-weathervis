# Stdlib imports
# Core Django imports
from django.contrib.gis import admin

# Third-party app imports
# Imports from my apps
from .models import DomainsPlot, StationsPlot

admin.site.register(StationsPlot)
admin.site.register(DomainsPlot)
