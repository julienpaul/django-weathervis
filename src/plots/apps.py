# Stdlib imports
# Core Django imports
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

# Third-party app imports
# Imports from my app


class StationsPlotsConfig(AppConfig):
    name = "src.plots"
    verbose_name = _("StationsPlots")


class DomainsPlotsConfig(AppConfig):
    name = "src.plots"
    verbose_name = _("DomainsPlots")
