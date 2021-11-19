# Stdlib imports
# Core Django import
from django.urls import path

# Third-party app imports
# Imports from my apps
from .views import margin_confirm_delete_view, margin_view

app_name = "margins"
urlpatterns = [
    path("", view=margin_view, name="list"),
    path("~delete/<pk>/", view=margin_confirm_delete_view, name="delete"),
]
