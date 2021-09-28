# Stdlib imports
# Core Django imports
from django.contrib.postgres.fields import CICharField
from django.db import models
from django.utils.translation import gettext_lazy as _

# Third-party app imports
# Imports from my apps


class Organisation(models.Model):

    name = CICharField(
        _("name"),
        max_length=150,
        unique=True,
        help_text=_("Required. 150 characters or fewer. Case insensitive."),
        error_messages={
            "unique": _("An organisation with that name already exists."),
        },
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
