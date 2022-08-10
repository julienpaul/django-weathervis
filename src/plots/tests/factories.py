# Stdlib imports
# Core Django imports
# Third-party app imports
from factory import Faker as FactoryFaker
from factory.django import DjangoModelFactory

# Imports from my apps
from src.plots.models import StationsPlot


class StationsPlotFactory(DjangoModelFactory):
    class Meta:
        model = StationsPlot

    name = FactoryFaker("company")
    command = FactoryFaker("sentence", nb_words=5)
    options = FactoryFaker("sentence", nb_words=5)
    description = FactoryFaker("sentence", nb_words=40)
