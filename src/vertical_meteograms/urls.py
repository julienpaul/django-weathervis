# Stdlib imports
# Core Django import
from django.urls import path

# Third-party app imports
# Imports from my apps
from .views import (  # select_location,; select_date,; select_type,
    change_plot,
    show_plot,
    vmeteogram_create_view,
    vmeteogram_list_view,
    vmeteogram_redirect_view,
    vmeteogram_update_view,
)

app_name = "vmeteograms"
urlpatterns = [
    path("", view=vmeteogram_redirect_view, name="redirect"),
    path("list", view=vmeteogram_list_view, name="list"),
    path("~add/", view=vmeteogram_create_view, name="create"),
    path("<slug>/", view=vmeteogram_update_view, name="detail"),
    path("ajax/change_plot/", change_plot, name="change_plot"),
    # path("ajax/select_location/", select_location, name="select_location"),
    # path("ajax/select_date/", select_date, name="select_date"),
    # path("ajax/select_type/", select_type, name="select_type"),
    path("ajax/show_plot/", show_plot, name="show_plot"),
]
