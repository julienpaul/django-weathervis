# Stdlib imports
# Core Django imports
# Third-party app imports
from factory import fuzzy as FactoryFuzzy
from factory.django import DjangoModelFactory

# Imports from my apps
from src.margins.models import Margin


class MarginFactory(DjangoModelFactory):
    class Meta:
        model = Margin

    west = FactoryFuzzy.FuzzyDecimal(low=0, high=180, precision=6)
    east = FactoryFuzzy.FuzzyDecimal(low=0, high=180, precision=6)
    north = FactoryFuzzy.FuzzyDecimal(low=0, high=90, precision=6)
    south = FactoryFuzzy.FuzzyDecimal(low=0, high=90, precision=6)
