# Stdlib imports
from pathlib import Path

# Core Django imports
from django.conf import settings
from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _
from django_extensions.db.fields import AutoSlugField

# Third-party app imports
# Imports from my apps
from src.stations.models import Station
from src.utils.storage import OverwriteStorage
from src.vertical_meteograms.models import VMDate


class SMType(models.Model):
    class Options(models.TextChoices):
        choice1 = "op1", _("Synoptics")
        choice2 = "op2", _("Precipitation")

    name = models.CharField(
        max_length=3,
        choices=Options.choices,
        default=Options.choice1,
    )

    class Meta:
        verbose_name = "Surface Meteogram Type"
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "name",
                ],
                name="unique_smeteogram_type",
            ),
        ]

    def __str__(self):
        """"""
        # get_FOO_display(),
        # see https://docs.djangoproject.com/en/3.2/ref/models/instances/#django.db.models.Model.get_FOO_display
        return f"{self.get_name_display():<13}"


class SMPoints(models.Model):
    class Options(models.TextChoices):
        choice1 = "HERE", _("Point location")
        choice2 = "ALL", _("All points")
        choice3 = "LAND", _("Land points")
        choice4 = "SEA", _("Sea points")
        # choice5 = "NEAR", _("Nearest point")

    name = models.CharField(
        max_length=4,
        choices=Options.choices,
        default=Options.choice1,
    )

    class Meta:
        verbose_name = "Surface Meteogram Point"
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "name",
                ],
                name="unique_smeteogram_points",
            ),
        ]

    def __str__(self):
        """"""
        return f"{self.get_name_display():<14}"


class SurfaceMeteogram(models.Model):
    slug = AutoSlugField(
        "Surface Meteogram Adress",
        unique=True,
        # always_update=False,
        populate_from=["location", "type", "points", "date"],
    )
    type = models.ForeignKey(
        SMType,
        on_delete=models.CASCADE,
    )
    points = models.ForeignKey(
        SMPoints,
        on_delete=models.CASCADE,
    )

    location = models.ForeignKey(
        Station,
        on_delete=models.CASCADE,
    )

    date = models.ForeignKey(
        VMDate,
        on_delete=models.CASCADE,
    )

    img_height = models.PositiveIntegerField(default=0)
    img_width = models.PositiveIntegerField(default=0)

    img = models.ImageField(
        upload_to="pics/PMET",
        default="pics/default.svg",
        height_field=None,
        width_field=None,
        storage=OverwriteStorage(),
    )

    class Meta:
        verbose_name = "Surface Meteogram"
        ordering = ["date", "location", "type", "points"]

    def __str__(self):
        return f"{self.date.date.strftime('%Y%m%d:%H'):<14} {self.type} {self.location}"

    def save(self, *args, **kwargs):
        """overwrite save to load imgage"""
        if self.img == "pics/default.svg":

            # date format: YYYYMMDDHH
            _date = self.date.date.strftime("%Y%m%d%H")

            if self.points.name == "HERE":
                img_path = f"weathervis/{_date}/PMET_{self.location}_{_date}_{self.type.name}.png"
            else:
                img_path = f"weathervis/{_date}/PMET_{self.location}_{_date}_{self.type.name}_{self.points.name}.png"
            if Path(Path(settings.MEDIA_ROOT) / img_path).exists():
                # if exist, overwrite path to image
                self.img = img_path
        super().save(*args, **kwargs)  # Call the "real" save() method.
