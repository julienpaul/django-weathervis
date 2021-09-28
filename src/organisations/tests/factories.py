from factory import Faker
from factory.django import DjangoModelFactory

from src.organisations.models import Organisation


class OrganisationFactory(DjangoModelFactory):
    name = Faker("company")

    class Meta:
        model = Organisation
