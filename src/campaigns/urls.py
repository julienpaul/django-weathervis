# Stdlib imports
# Core Django import
from django.urls import path

# Third-party app imports
# Imports from my apps
from .views import (
    campaign_confirm_delete_view,
    campaign_create_view,
    campaign_list_view,
    campaign_update_view,
)

app_name = "campaigns"
urlpatterns = [
    path("", view=campaign_list_view, name="list"),
    path("~add/", view=campaign_create_view, name="create"),
    path("~delete/<pk>/", view=campaign_confirm_delete_view, name="delete"),
    path("~update/<pk>/", view=campaign_update_view, name="update"),
]
