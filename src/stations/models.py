# Stdlib imports
# Core Django imports
from django.contrib.auth import get_user_model
from django.contrib.gis.db import models
from django.contrib.postgres.fields import CICharField
from django.utils.translation import gettext_lazy as _
from django_extensions.db.fields import AutoSlugField

# Third-party app imports
# Imports from my apps
from src.margins.models import Margin

User = get_user_model()

# TODO look to add default Margin


class Station(models.Model):
    name = CICharField(
        max_length=50,
        unique=True,
        error_messages={
            "unique": _("That name already exists."),
        },
    )
    slug = AutoSlugField(
        "Station Adress",
        unique=True,
        # always_update=False,
        populate_from="name",
    )
    # GeoDjango-specific: a geometry field (MultiPolygonField)
    geom = models.PointField(srid=4326, dim=3)
    # geom = models.PointField(geography=True, default=geoPoint(0.0, 0.0))
    #
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    #
    station_id = CICharField(
        max_length=50,
        unique=True,
        blank=True,
        null=True,
        help_text="Station identifier",
        error_messages={
            "unique": _("That station_id already exists."),
        },
    )
    wmo_id = CICharField(
        max_length=5,
        unique=True,
        blank=True,
        null=True,
        help_text="WMO identifier",
        error_messages={
            "unique": _("That wmo_id already exists."),
        },
    )
    description = models.TextField(
        blank=True,
        help_text="Add information about the station",
    )
    margin = models.ForeignKey(
        Margin,
        on_delete=models.RESTRICT,
        related_name="stations",
        help_text="Offset around station location",
        # default=
    )
    margin_geom = models.PolygonField(dim=3, srid=4326)

    is_active = models.BooleanField(default=True)

    # model = model to use for plot or list of model who contains this station ??
    class Meta:
        ordering = ["name"]

    # def save(self, *args, **kwargs):
    #     try:
    #         self.margin
    #     except:
    #         self.margin = Margin.objects.first()
    #     super().save(*args, **kwargs)
    #
    # def calculate_default(self):
    #     default = (self.field_1 + self.field_2) / 2
    #     return default
    # def save(self, *args, **kwargs):
    #     if self.score == None:
    #        self.score = self.calculate_default()
    #     super().save(*args, **kwargs)

    # Returns the string representation of the model.
    def __str__(self):
        return self.name

    @property
    def longitude(self):
        return self.geom.x

    @property
    def latitude(self):
        return self.geom.y

    @property
    def altitude(self):
        return self.geom.z

    def save(self, *args, **kwargs):
        """ """
        from .load import down as download

        super().save(*args, **kwargs)
        # update weathervis config files
        download()
