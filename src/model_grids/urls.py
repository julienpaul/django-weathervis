# Stdlib imports
# Core Django imports
from django.urls import path

# Third-party app imports
# Imports from my apps
from .views import all_grids

app_name = "model_grids"
urlpatterns = [
    path("ajax/data_all_grids/", all_grids, name="all_grids"),
]
