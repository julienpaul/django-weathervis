# Stdlib imports
# Core Django imports
from django.core.serializers import serialize
from django.http import HttpResponse

# Third-party app imports
# Imports from my apps
from .models import ModelGrid


def all_grids(request):
    """this uses the serializer to convert the data 'ModelGrid.objects.all()' to 'geojson' data"""
    grid = serialize(
        "geojson",
        ModelGrid.objects.all(),
    )
    return HttpResponse(grid, content_type="json")
