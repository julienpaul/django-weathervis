# Stdlib imports
# Core Django import
from django.urls import path

# Third-party app imports
# Imports from my apps
from .views import (  # select_location,; select_date,; select_type,
    change_plot,
    show_plot,
    smeteogram_create_view,
    smeteogram_list_view,
    smeteogram_redirect_view,
    smeteogram_update_view,
)

app_name = "smeteograms"
urlpatterns = [
    path("", view=smeteogram_redirect_view, name="redirect"),
    path("list/", view=smeteogram_list_view, name="list"),
    path("~add/", view=smeteogram_create_view, name="create"),
    path("<slug>/", view=smeteogram_update_view, name="detail"),
    path("ajax/change_plot/", change_plot, name="change_plot"),
    path("ajax/show_plot/", show_plot, name="show_plot"),
]
