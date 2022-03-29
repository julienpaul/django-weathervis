# Stdlib imports
# Core Django imports
from django.contrib import admin

# Third-party app imports
# Imports from my apps
from .models import SMPoints, SMType, SurfaceMeteogram

admin.site.register(SurfaceMeteogram)
admin.site.register(SMType)
admin.site.register(SMPoints)
