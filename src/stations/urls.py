# Stdlib imports
# Core Django imports
from django.urls import path

# Third-party app imports
# Imports from my apps
from .views import (
    change_campaign,
    data_all_stations,
    data_this_station_margin,
    disable_all_stations,
    download_config,
    enable_all_stations,
    station_campaign_detail_list_view,
    station_confirm_delete_view,
    station_create_view,
    station_detail_list_view,
    station_detail_view,
    station_list_view,
    station_redirect_view,
    station_update_view,
)

app_name = "stations"
urlpatterns = [
    path("~redirect/", view=station_redirect_view, name="redirect"),
    path("~list/", view=station_list_view, name="list"),
    path("~add/", view=station_create_view, name="create"),
    path("~disable_all_stations/", disable_all_stations, name="disable"),
    path("~download_config/", download_config, name="download"),
    path("~enable_all_stations/", enable_all_stations, name="enable"),
    path("@<slug>/", view=station_detail_list_view, name="detail_list"),
    path(
        "#<pk>/@<slug>",
        view=station_campaign_detail_list_view,
        name="campaign_detail_list",
    ),
    # path("#<slug>/", view=station_list2_view, name="detail"),
    path("~detail/<slug>/", view=station_detail_view, name="detail"),
    path("~update/<slug>/", view=station_update_view, name="update"),
    path("~delete/<slug>/", view=station_confirm_delete_view, name="delete"),
    #
    path("ajax/data_this_margin/<slug>/", data_this_station_margin, name="this_margin"),
    path("ajax/data_all_stations/", data_all_stations, name="all_stations"),
    path("ajax/change_campaign/", change_campaign, name="change_campaign"),
]
