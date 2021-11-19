# Stdlib imports
# Core Django imports
# Third-party app imports
from factory import Faker as FactoryFaker
from factory.django import DjangoModelFactory

# Imports from my apps
from src.organisations.models import Organisation


class OrganisationFactory(DjangoModelFactory):
    class Meta:
        model = Organisation

    name = FactoryFaker("company")
