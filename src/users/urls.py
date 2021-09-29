# Stdlib imports
# Core Django imports
from django.urls import path

# Third-party app imports
# Imports from my apps
from src.users.views import (
    user_detail_view,
    user_redirect_view,
    user_update_view,
    user_upgrade_request_view,
)

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("@<str:username>/", view=user_detail_view, name="detail"),
    path("~upgrade/request/", view=user_upgrade_request_view, name="upgrade_request"),
]
