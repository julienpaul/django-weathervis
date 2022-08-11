# Stdlib imports
# Core Django imports
from django.urls import path

# Third-party app imports
# Imports from my apps
from .views import (
    data_all_domains,
    data_this_domain,
    domain_confirm_delete_view,
    domain_create_view,
    domain_detail_list_view,
    domain_detail_view,
    domain_list_view,
    domain_redirect_view,
    domain_update_view,
)

app_name = "domains"
urlpatterns = [
    path("~redirect/", view=domain_redirect_view, name="redirect"),
    path("~list/", view=domain_list_view, name="list"),
    path("~add/", view=domain_create_view, name="create"),
    path("<slug>/", view=domain_detail_list_view, name="detail_list"),
    path("~detail/<slug>/", view=domain_detail_view, name="detail"),
    path("~update/<slug>/", view=domain_update_view, name="update"),
    path("~delete/<slug>/", view=domain_confirm_delete_view, name="delete"),
    #
    path("ajax/data_all_domains/", data_all_domains, name="all_domains"),
    path("ajax/data_this_domain/<slug>/", data_this_domain, name="this_domain"),
]
