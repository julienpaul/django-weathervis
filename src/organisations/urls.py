# Stdlib imports
# Core Django import
from django.urls import path

# Third-party app imports
# Imports from my apps
from .views import organisation_confirm_delete_view, organisation_view

app_name = "organisations"
urlpatterns = [
    path("", view=organisation_view, name="list"),
    path("~delete/<pk>/", view=organisation_confirm_delete_view, name="delete"),
]
