"""
Module for all Form Tests.
"""
# Stdlib imports
import pytest

# Core Django imports
from django.utils.translation import gettext_lazy as _

# Third-party app imports
# Imports from my apps
from src.users.forms import UserCreationForm, UserUpdateForm
from src.users.models import User

pytestmark = pytest.mark.django_db


class TestUserCreationForm:
    """
    Test class for all tests related to the UserCreationForm
    """

    def test_username_validation_error_msg(self, user: User):
        """
        Tests UserCreation Form's unique validator functions correctly by testing:
            1) A new user with an existing username cannot be added.
            2) Only 1 error is raised by the UserCreation Form
            3) The desired error message is raised
        """

        # The user already exists,
        # hence cannot be created.
        data = {
            "username": user.username,
            "email": "another@mail.com",
            "password1": user.password,
            "password2": user.password,
        }
        form = UserCreationForm(data)

        assert not form.is_valid()
        assert len(form.errors) == 1
        assert "username" in form.errors
        assert form.errors["username"][0] == _(
            "A user with that username already exists."
        )

    def test_username_case_sensitive_validation_error_msg(self, user: User):
        """
        Tests UserCreation Form's unique validator functions correctly by testing:
            1) A new user with an existing username cannot be added.
            2) Only 1 error is raised by the UserCreation Form
            3) The desired error message is raised
        """
        # The user already exists,
        # hence cannot be created.
        data = {
            "username": user.username.upper(),
            "email": "another@mail.com",
            "password1": user.password,
            "password2": user.password,
        }
        form = UserCreationForm(data)

        assert not form.is_valid()
        assert len(form.errors) == 1
        assert "username" in form.errors
        assert form.errors["username"][0] == _(
            "A user with that username already exists."
        )

    def test_email_validation_error_msg(self, user: User):
        """
        Tests UserCreation Form's unique validator functions correctly by testing:
            1) A new user with an existing email cannot be added.
            2) Only 1 error is raised by the UserCreation Form
            3) The desired error message is raised
        """
        # The user already exists,
        # hence cannot be created.
        data = {
            "username": "another_username",
            "email": user.email,
            "password1": user.password,
            "password2": user.password,
        }
        form = UserCreationForm(data)

        assert not form.is_valid()
        assert len(form.errors) == 1
        assert "email" in form.errors
        assert form.errors["email"][0] == _(
            "A user with that email address already exists."
        )

    def test_email_case_sensitive_validation_error_msg(self, user: User):
        """
        Tests UserCreation Form's unique validator functions correctly by testing:
            1) A new user with an existing email cannot be added.
            2) Only 1 error is raised by the UserCreation Form
            3) The desired error message is raised
        """
        # The user already exists,
        # hence cannot be created.
        data = {
            "username": "another_username",
            "email": user.email.upper(),
            "password1": user.password,
            "password2": user.password,
        }
        form = UserCreationForm(data)

        assert not form.is_valid()
        assert len(form.errors) == 1
        assert "email" in form.errors
        assert form.errors["email"][0] == _(
            "A user with that email address already exists."
        )


class TestUserUpdateForm:
    """
    Test class for all tests related to the UserUpdateForm
    """

    def test_init_helper(self):
        """
        GIVEN class UserUpdateForm
        WHEN  initialised an instance
        THEN  instance should have attribute 'helper' and 'helper.layout'
        """
        form = UserUpdateForm()
        assert hasattr(form, "helper")
        assert hasattr(form.helper, "layout")
