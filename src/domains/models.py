# Stdlib imports
# Core Django imports
from django.contrib.auth import get_user_model
from django.contrib.gis.db import models
from django.contrib.postgres.fields import CICharField
from django.utils.translation import gettext_lazy as _
from django_extensions.db.fields import AutoSlugField

# Third-party app imports
# Imports from my apps

User = get_user_model()


class Domain(models.Model):
    name = CICharField(
        max_length=50,
        unique=True,
        error_messages={
            "unique": _("That name already exists."),
        },
    )
    slug = AutoSlugField(
        "Domain Adress",
        unique=True,
        # always_update=False,
        populate_from="name",
    )
    # GeoDjango-specific: a geometry field (MultiPolygonField)
    geom = models.PolygonField(srid=4326, dim=3)
    #
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    #
    description = models.TextField(
        blank=True,
        help_text="Add information about the domain",
    )
    is_active = models.BooleanField(default=True)

    # model = model to use for plot or list of model who contains this station ??
    class Meta:
        ordering = ["name"]

    # Returns the string representation of the model.
    def __str__(self):
        return self.name

    @property
    def west(self):
        return self.geom.extent[0]

    @property
    def south(self):
        return self.geom.extent[1]

    @property
    def east(self):
        return self.geom.extent[2]

    @property
    def north(self):
        return self.geom.extent[3]

    @property
    def altitude(self):
        return self.geom.coords[0][0][2]
