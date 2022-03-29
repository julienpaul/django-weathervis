# Stdlib imports
import random

# Core Django imports
from django.core.files.base import ContentFile

# Third-party app imports
from factory import LazyAttribute, LazyFunction, SubFactory
from factory.django import DjangoModelFactory, ImageField

# Imports from my apps
from src.stations.tests.factories import StationFactory
from src.surface_meteograms.models import SMPoints, SMType, SurfaceMeteogram
from src.vertical_meteograms.tests.factories import VMDateFactory


class SMTypeFactory(DjangoModelFactory):
    class Meta:
        model = SMType

    name = LazyFunction(lambda: random.choice(SMType.Options.choices)[0])


class SMPointsFactory(DjangoModelFactory):
    class Meta:
        model = SMPoints

    name = LazyFunction(lambda: random.choice(SMType.Options.choices)[0])


class SurfaceMeteogramFactory(DjangoModelFactory):
    class Meta:
        model = SurfaceMeteogram

    type = SubFactory(SMTypeFactory)
    points = SubFactory(SMPointsFactory)

    location = SubFactory(StationFactory)

    date = SubFactory(VMDateFactory)

    img_height = 0
    img_width = 0

    img = LazyAttribute(
        lambda _: ContentFile(
            ImageField()._make_data({"width": 750, "height": 800}), "example.png"
        )
    )
