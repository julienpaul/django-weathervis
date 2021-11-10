from factory import Faker as FactoryFaker
from factory.django import DjangoModelFactory

from src.organisations.models import Organisation


class OrganisationFactory(DjangoModelFactory):
    name = FactoryFaker("company")

    class Meta:
        model = Organisation
