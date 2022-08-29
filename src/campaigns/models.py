# Stdlib imports
# Core Django imports
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import CICharField
from django.db import models
from django.utils.translation import gettext_lazy as _

# Third-party app imports
# Imports from my apps

User = get_user_model()


class Campaign(models.Model):

    name = CICharField(
        _("name"),
        max_length=150,
        unique=True,
        help_text=_("Required. 150 characters or fewer. Case insensitive."),
        error_messages={
            "unique": _("A campaign with that name already exists."),
        },
    )
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    description = models.TextField(
        blank=True,
        help_text="Add information about the station plot",
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
