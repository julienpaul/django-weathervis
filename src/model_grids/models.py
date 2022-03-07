# Stdlib imports
# Core Django imports
from django.contrib.auth import get_user_model
from django.contrib.gis.db import models
from django_extensions.db.fields import AutoSlugField

# Third-party app imports
# Imports from my apps

User = get_user_model()


class ModelGrid(models.Model):
    #
    name = models.CharField(
        max_length=50,
    )
    slug = AutoSlugField(
        "ModelGrid name",
        unique=True,
        # always_update=False,
        populate_from="name",
    )
    # GeoDjango-specific: a geometry field (MultiPolygonField)
    geom = models.PolygonField(dim=3, srid=4326)
    #
    created_at = models.DateTimeField(auto_now_add=True)
    # created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date_valid_start = models.DateTimeField(null=True)
    date_valid_end = models.DateTimeField(null=True)
    leadtime = models.DurationField(null=True)  # datetime.timedelta(hours=66)

    class Meta:
        ordering = ["name", "date_valid_start"]
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "name",
                    "date_valid_start",
                ],
                name="unique_model_grid",
            ),
        ]

    # Returns the string representation of the model.
    def __str__(self):
        return f"{self.name}, {self.date_valid_start}"


class ModelVariable(models.Model):
    #
    name = models.CharField(max_length=150)
    slug = AutoSlugField(
        "Variable name",
        unique=True,
        # always_update=False,
        populate_from="name",
    )
    model_grid = models.ForeignKey(ModelGrid, on_delete=models.CASCADE)
    # level

    class Meta:
        ordering = ["model_grid", "name"]
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "name",
                    "model_grid",
                ],
                name="unique_variable",
            ),
        ]

    # Returns the string representation of the model.
    def __str__(self):
        return f"{self.name} ({self.model_grid})"
