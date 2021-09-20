# Stdlib imports
from typing import Any, Sequence

# Core Django imports
from django.contrib.auth import get_user_model

# Third-party app imports
from factory import Faker, Trait, post_generation
from factory.django import DjangoModelFactory

# Imports from my apps


class UserFactory(DjangoModelFactory):

    username = Faker("user_name")
    email = Faker("email")
    name = Faker("name")
    is_staff = False
    is_superuser = False

    @post_generation
    def password(self, create: bool, extracted: Sequence[Any], **kwargs):
        password = (
            extracted
            if extracted
            else Faker(
                "password",
                length=42,
                special_chars=True,
                digits=True,
                upper_case=True,
                lower_case=True,
            ).evaluate(None, None, extra={"locale": None})
        )
        self.set_password(password)

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
