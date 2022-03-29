# Stdlib imports
import random

# Core Django imports
from django.core.files.base import ContentFile

# Third-party app imports
from factory import Faker as FactoryFaker
from factory import LazyAttribute, LazyFunction, SubFactory
from factory.django import DjangoModelFactory, ImageField

# Imports from my apps
from src.stations.tests.factories import StationFactory
from src.vertical_meteograms.models import VerticalMeteogram, VMDate, VMType


class VMTypeFactory(DjangoModelFactory):
    class Meta:
        model = VMType

    name = LazyFunction(lambda: random.choice(VMType.Options.choices)[0])


class VMDateFactory(DjangoModelFactory):
    class Meta:
        model = VMDate

    date = FactoryFaker("date_time")


class VerticalMeteogramFactory(DjangoModelFactory):
    class Meta:
        model = VerticalMeteogram

    type = SubFactory(VMTypeFactory)

    location = SubFactory(StationFactory)

    date = SubFactory(VMDateFactory)

    img_height = 0
    img_width = 0

    img = LazyAttribute(
        lambda _: ContentFile(
            ImageField()._make_data({"width": 750, "height": 800}), "example.png"
        )
    )
