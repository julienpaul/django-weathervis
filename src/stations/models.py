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
from src.campaigns.models import Campaign
from src.margins.models import Margin
from src.plots.models import StationsPlot

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

    # Plots create for active station only
    is_active = models.BooleanField(default=True)

    # list of plots available for the station
    plots = models.ManyToManyField(
        StationsPlot,
        blank=True,
        related_name="stations",
    )

    # list of campaigns associated with the station
    campaigns = models.ManyToManyField(
        Campaign,
        blank=True,
        related_name="stations",
    )
    # which campaign is currently active
    active_campaign = models.IntegerField(blank=True, null=True)

    # Flexpart
    uses_flexpart = models.BooleanField(default=False)

    start_datetime = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Starting date of the release",
    )
    end_datetime = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Ending date of the release",
    )

    class AltUnit(models.IntegerChoices):
        METER = 1, _("m (a.g.l)")
        PASCAL = 2, _("m (a.s.l)")
        HECTOPASCAL = 3, _("hPa")

    alt_lower = models.DecimalField(
        default=0,
        max_digits=6,
        decimal_places=2,
    )
    alt_upper = models.DecimalField(
        default=0,
        max_digits=6,
        decimal_places=2,
        help_text="Upper altitude of the release",
    )
    alt_unit = models.IntegerField(
        default=1,
        choices=AltUnit.choices,
        help_text="Altitude unit",
    )
    numb_part = models.PositiveIntegerField(
        default=5000,
    )
    xmass = models.PositiveIntegerField(
        default=100,
    )
    number_grid = models.PositiveIntegerField(
        default=200,
    )
    # model = model to use for plot or list of model who contains this station ??

    class Meta:
        ordering = ["name"]

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
        super().save(*args, **kwargs)
        #
        if self.active_campaign:
            self.campaigns.add(self.active_campaign)
        from .util import download

        download()

    def delete(self, *args, **kwargs):
        """ """
        super().delete(*args, **kwargs)
        from .util import download

        download()

    @classmethod
    def disable_all(cls, campaign_id=None):
        if campaign_id:
            cls.objects.filter(campaigns=campaign_id).update(is_active=False)
        else:
            cls.objects.update(is_active=False)
        # for obj in cls.objects.all():
        #     obj.is_active = False
        #     obj.save()

    @classmethod
    def enable_all(cls, campaign_id=None):
        if campaign_id:
            cls.objects.filter(campaigns=campaign_id).update(is_active=True)
        else:
            cls.objects.update(is_active=True)

    @classmethod
    def active_campaign_is(cls, campaign_id=None):
        cls.objects.update(active_campaign=campaign_id)


@receiver(m2m_changed, sender=Station.plots.through)
def update_station_m2m(sender, instance, action, reverse, *args, **kwargs):
    """wait until change in Many2Many field get saved"""
    # https://stackoverflow.com/a/57308547
    if "post" in action:
        from .util import download

        download()
