# Stdlib imports
# Core Django imports
from django.contrib import admin

# Third-party app imports
# Imports from my apps
from .models import Campaign

admin.site.register(Campaign)
