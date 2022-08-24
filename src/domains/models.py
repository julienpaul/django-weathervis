# Stdlib imports
# Core Django imports
from django.contrib.auth import get_user_model
from django.contrib.gis.db import models
from django.contrib.postgres.fields import CICharField
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django_extensions.db.fields import AutoSlugField

# Third-party app imports
# Imports from my apps
from src.plots.models import DomainsPlot

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

    # list of plots available for the station
    plots = models.ManyToManyField(
        DomainsPlot,
        blank=True,
        related_name="domains",
    )

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

    def save(self, *args, **kwargs):
        """ """
        super().save(*args, **kwargs)
        from .util import download

        download()

    def delete(self, *args, **kwargs):
        """ """
        super().save(*args, **kwargs)
        from .util import download

        download()

    @classmethod
    def disable_all(cls):
        cls.objects.update(is_active=False)

    @classmethod
    def enable_all(cls):
        cls.objects.update(is_active=True)


@receiver(m2m_changed, sender=Domain.plots.through)
def update_domain_m2m(sender, instance, action, reverse, *args, **kwargs):
    """wait until change in Many2Many field get saved"""
    # https://stackoverflow.com/a/57308547
    if "post" in action:
        from .util import download

        download()
