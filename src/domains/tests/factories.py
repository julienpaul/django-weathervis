# Stdlib imports
# Core Django imports
# Third-party app imports
from factory import Faker as FactoryFaker
from factory.django import DjangoModelFactory

# Imports from my apps
from src.domains.models import Domain
from src.utils.tests.factories import DjangoGeoBBoxProvider


class DomainFactory(DjangoModelFactory):
    class Meta:
        model = Domain

    FactoryFaker.add_provider(DjangoGeoBBoxProvider)

    name = FactoryFaker("company")
    geom = FactoryFaker("geo_bbox")
    description = FactoryFaker("sentence", nb_words=40)
