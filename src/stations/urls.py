# Stdlib imports
# Core Django imports
from django.urls import path

# Third-party app imports
# Imports from my apps
from .views import (
    data_all_stations,
    data_this_station_margin,
    station_confirm_delete_view,
    station_create_view,
    station_detail_view,
    station_list_view,
    station_redirect_view,
    station_update_view,
)

app_name = "stations"
urlpatterns = [
    path("", view=station_list_view, name="list"),
    path("~redirect/<slug>/", view=station_redirect_view, name="redirect"),
    path("~add/", view=station_create_view, name="create"),
    path("<slug>/", view=station_detail_view, name="detail"),
    path("<slug>/~update/", view=station_update_view, name="update"),
    path("~delete/<slug>/", view=station_confirm_delete_view, name="delete"),
    #
    path("ajax/data_this_margin/<slug>/", data_this_station_margin, name="this_margin"),
    path("ajax/data_all_stations/", data_all_stations, name="all_stations"),
]
