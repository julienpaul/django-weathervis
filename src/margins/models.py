# Stdlib imports
# Core Django imports
from django.contrib.gis.db import models

# Third-party app imports
# Imports from my apps
from src.utils.util import degree_sign as deg


class Margin(models.Model):
    west = models.DecimalField(max_digits=9, decimal_places=6, default=0.2)
    east = models.DecimalField(max_digits=9, decimal_places=6, default=0.2)
    north = models.DecimalField(max_digits=8, decimal_places=6, default=0.2)
    south = models.DecimalField(max_digits=8, decimal_places=6, default=0.2)

    class Meta:
        verbose_name = "Margin"
        ordering = ["west", "east", "north", "south"]
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "west",
                    "east",
                    "north",
                    "south",
                ],
                name="unique_margin",
            ),
        ]

    def __str__(self):
        return f"{self.west}{deg}W | {self.east}{deg}E | {self.north}{deg}N | {self.south}{deg}S"
