# Stdlib imports
# Core Django imports
from django.contrib.auth import get_user_model
from django.contrib.gis.db import models
from django.contrib.postgres.fields import CICharField
from django.utils.translation import gettext_lazy as _

# Third-party app imports
# Imports from my apps

User = get_user_model()


class StationsPlot(models.Model):
    name = CICharField(
        max_length=250,
        unique=True,
        error_messages={
            "unique": _("That name already exists."),
        },
    )

    command = models.CharField(blank=True, max_length=255)
    options = models.CharField(blank=True, max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    description = models.TextField(
        blank=True,
        help_text="Add information about the station plot",
    )

    # Returns the string representation of the model.
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """ """
        super().save(*args, **kwargs)
        # update weathervis config files
        from .util import download

        download()

    def delete(self, *args, **kwargs):
        """ """
        super().delete(*args, **kwargs)
        # update weathervis config files
        from src.stations.util import download as download_station

        from .util import download

        download()
        download_station()


class DomainsPlot(models.Model):
    name = CICharField(
        max_length=250,
        unique=True,
        error_messages={
            "unique": _("That name already exists."),
        },
    )

    command = models.CharField(blank=True, max_length=255)
    options = models.CharField(blank=True, max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    description = models.TextField(
        blank=True,
        help_text="Add information about the domain plot",
    )

    # Returns the string representation of the model.
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """ """
        super().save(*args, **kwargs)
        # update weathervis config files
        from .util import download

        download()

    def delete(self, *args, **kwargs):
        """ """
        super().delete(*args, **kwargs)
        # update weathervis config files
        from src.domains.util import download as download_domain

        from .util import download

        download()
        download_domain()
