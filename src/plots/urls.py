# Stdlib imports
# Core Django imports
from django.urls import path

# Third-party app imports
# Imports from my apps
from .views import (
    domains_plot_confirm_delete_view,
    domains_plot_create_view,
    domains_plot_list_view,
    domains_plot_update_view,
    stations_plot_confirm_delete_view,
    stations_plot_create_view,
    stations_plot_list_view,
    stations_plot_update_view,
)

app_name = "plots"
urlpatterns = [
    path("stations/", view=stations_plot_list_view, name="stations_list"),
    path("stations/~add/", view=stations_plot_create_view, name="stations_create"),
    path(
        "stations/~update/<pk>/", view=stations_plot_update_view, name="stations_update"
    ),
    path(
        "stations/~delete/<pk>/",
        view=stations_plot_confirm_delete_view,
        name="stations_delete",
    ),
    path("domains/", view=domains_plot_list_view, name="domains_list"),
    path("domains/~add/", view=domains_plot_create_view, name="domains_create"),
    path("domains/~update/<pk>/", view=domains_plot_update_view, name="domains_update"),
    path(
        "domains/~delete/<pk>/",
        view=domains_plot_confirm_delete_view,
        name="domains_delete",
    ),
]
