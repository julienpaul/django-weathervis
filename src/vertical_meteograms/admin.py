# Stdlib imports
# Core Django imports
from django.contrib import admin

# Third-party app imports
# Imports from my apps
from .models import VerticalMeteogram, VMDate, VMType

admin.site.register(VerticalMeteogram)
admin.site.register(VMType)
admin.site.register(VMDate)
