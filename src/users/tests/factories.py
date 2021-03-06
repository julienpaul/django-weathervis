# Stdlib imports
from typing import Any, Sequence

# Core Django imports
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission

# Third-party app imports
from factory import Faker as FactoryFaker
from factory import SubFactory, Trait, post_generation
from factory.django import DjangoModelFactory

# Imports from my apps
from src.organisations.tests.factories import OrganisationFactory


def get_group(name_):
    """Returns the name_ Group"""
    try:
        group_obj = Group.objects.get(name__iexact=name_)
    except Group.DoesNotExist:
        raise ValueError(f"No Group {name_}")
    return group_obj


def get_permission(name_):
    """Returns the name_ Permission"""
    try:
        permission = Permission.objects.get(
            codename=f"change_{name_}",
        )
    except Permission.DoesNotExist:
        raise ValueError(f"No Permission {name_}")
    return permission


class UserFactory(DjangoModelFactory):
    class Meta:
        model = get_user_model()
        django_get_or_create = ["username"]

    class Params:
        staff = Trait(
            is_staff=True,
            is_superuser=False,
        )
        superuser = Trait(
            is_staff=True,
            is_superuser=True,
        )

    @post_generation
    def password(self, create: bool, extracted: Sequence[Any], **kwargs):
        password = (
            extracted
            if extracted
            else FactoryFaker(
                "password",
                length=42,
                special_chars=True,
                digits=True,
                upper_case=True,
                lower_case=True,
            ).evaluate(None, None, extra={"locale": None})
        )
        self.set_password(password)

    username = FactoryFaker("user_name")
    email = FactoryFaker("email")
    name = FactoryFaker("name")
    organisation = SubFactory(OrganisationFactory)
    is_staff = False
    is_superuser = False
