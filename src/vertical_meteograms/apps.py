# Stdlib imports
# Core Django imports
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

# Third-party app imports
# Imports from my app


class VerticalMeteogramsConfig(AppConfig):
    name = "src.vertical_meteograms"
    verbose_name = _("VerticalMeteograms")
