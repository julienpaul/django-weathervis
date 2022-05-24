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
from src.utils.util import read_subtext_file


class VMDate(models.Model):
    date = models.DateTimeField()
    # https://simpleisbetterthancomplex.com/tutorial/2019/01/03/how-to-use-date-picker-with-django.html
    # https://simpleisbetterthancomplex.com/references/2016/06/21/date-filter.html
    # https://stackoverflow.com/questions/10345147/django-query-datetime-for-objects-older-than-5-hours

    class Meta:
        verbose_name = "Vertical Meteogram Date and Time"
        ordering = ["date"]
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "date",
                ],
                name="unique_vmeteogram_date",
            ),
        ]

    def __str__(self):
        return f"{self.date}"


class VMType(models.Model):
    class Options(models.TextChoices):
        choice1 = "op1", _("Wind")
        choice2 = "op2", _("Clouds")

    name = models.CharField(
        max_length=3,
        choices=Options.choices,
        default=Options.choice1,
    )

    class Meta:
        verbose_name = "Vertical Meteogram Type"
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "name",
                ],
                name="unique_vmeteogram_type",
            ),
        ]

    def __str__(self):
        """"""
        # get_FOO_display(),
        # see https://docs.djangoproject.com/en/3.2/ref/models/instances/#django.db.models.Model.get_FOO_display
        return f"{self.get_name_display():<6}"


class VerticalMeteogram(models.Model):
    slug = AutoSlugField(
        "Vertical Meteogram Adress",
        unique=True,
        # always_update=False,
        populate_from=["location", "type", "date"],
    )
    type = models.ForeignKey(
        VMType,
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

    subtext = models.TextField(
        blank=True,
        null=True,
    )

    img_height = models.PositiveIntegerField(default=0)
    img_width = models.PositiveIntegerField(default=0)

    img = models.ImageField(
        upload_to="pics/VPMET",
        default="pics/default.svg",
        height_field=None,
        width_field=None,
        storage=OverwriteStorage(),
    )

    img_path = models.CharField(
        max_length=150,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Vertical Meteogram"
        ordering = ["date", "location", "type"]

    def __str__(self):
        return f"{self.date.date.strftime('%Y%m%d:%H'):<14} {self.type} {self.location}"

    def save(self, *args, **kwargs):
        """overwrite save to load imgage"""
        if self.img == "pics/default.svg":

            # date format: YYYYMMDDHH
            _date = self.date.date.strftime("%Y%m%d%H")

            self.img_path = (
                f"gfx/{_date}/VPMET_{self.location}_{_date}_{self.type.name}.png"
            )
            if Path(Path(settings.MEDIA_ROOT) / self.img_path).exists():
                # if exist, overwrite path to image
                self.img = self.img_path

        if self.subtext is None:
            self._get_subtext()

        super().save(*args, **kwargs)  # Call the "real" save() method.

    def _get_subtext(self):
        """get subtext from subtext.yaml"""
        plots = read_subtext_file()
        if "VerticalMeteogram" in plots:
            _ = plots["VerticalMeteogram"]
            self.subtext = _.get("subtext", None)
            if _ is not None and "type" in _:
                key = str(self.type).strip()
                _ = _["type"].get(key, None)
                if _ is not None and "subtext" in _:
                    self.subtext = _.get("subtext", None)
