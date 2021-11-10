# Stdlib imports
# Core Django imports
from django.contrib.auth import get_user_model
from django.contrib.gis.db import models

# Third-party app imports
# Imports from my apps

User = get_user_model()


class WeatherForecastBorder(models.Model):
    #
    name = models.CharField(max_length=50)
    # GeoDjango-specific: a geometry field (MultiPolygonField)
    geom = models.MultiPolygonField(srid=4326)
    #
    created_at = models.DateTimeField(auto_now_add=True)
    # created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ["name"]

    # Returns the string representation of the model.
    def __str__(self):
        return self.name
