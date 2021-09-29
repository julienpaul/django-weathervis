# Stdlib imports
import pytest
from crispy_forms.layout import Layout

# Core Django imports
from django.conf import settings
from django.core import mail
from django.test import RequestFactory
from django.utils.translation import gettext_lazy as _

# Third-party app imports
# Imports from my apps
from src.organisations.models import Organisation
from src.users.forms import UserCreationForm, UserUpdateForm, UserUpgradeForm
from src.users.models import User


class TestUserChangeForm:
    """
    Test class for all tests related to the UserChangeForm
    """


@pytest.mark.django_db
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

    @pytest.mark.skip(reason="test not implemented yet")
    def test_username_length_validation_error_msg(self):
        pass

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


@pytest.mark.django_db
class TestUserUpdateForm:
    """
    Test class for all tests related to the UserUpdateForm
    """

    def test_init_helper_layout(self):
        """
        GIVEN class UserUpdateForm
        WHEN  initialised an instance
        THEN  instance should have attribute 'helper' and 'helper.layout'
        """
        form = UserUpdateForm()
        assert hasattr(form, "helper")
        assert hasattr(form.helper, "layout")
        assert isinstance(form.helper.layout, Layout)

    @pytest.mark.skip(reason="test not implemented yet")
    def test_cripsy_form_inputs(self):
        """
        GIVEN class UserUpdateForm with a cripsy form
        WHEN  displaying the layout through a view instance
        THEN  the inputs should appear on the view
        """
        pass

    @pytest.mark.skip(reason="test not implemented yet")
    def test_cripsy_form_buttons(self):
        """
        GIVEN class UserUpdateForm with a cripsy form
        WHEN  displaying the layout through a view instance
        THEN  the buttons should appear on the view
        """
        pass

    @pytest.mark.skip(reason="test not implemented yet")
    def test_cripsy_form_redirect(self):
        """
        GIVEN class UserUpdateForm with a cripsy form
        WHEN  clicking on the button display on the view
        THEN  should be redirect to
        """
        pass


@pytest.mark.django_db
class TestUserUpgradeForm:
    """
    Test class for all tests related to the UserUpgradeForm
    """

    def test_init_helper_layout(self):
        """
        GIVEN class UserUpgradeForm
        WHEN  initialised an instance
        THEN  instance should have attribute 'helper' and 'helper.layout'
        """
        form = UserUpgradeForm()
        assert hasattr(form, "helper")
        assert hasattr(form.helper, "layout")
        assert isinstance(form.helper.layout, Layout)

    @pytest.mark.skip(reason="test not implemented yet")
    def test_custom_helper(self):
        pass

    def test_name_validation_error_msg(self, user: User):
        """
        GIVEN an instance of UserUpgradeForm
        WHEN  posting form with blank name
        THEN  should return error message
        """
        # The user already exists,
        # hence cannot be created.
        data = {
            "name": "",
            "organisation": user.organisation,
            "motivation": "blahblah",
        }
        form = UserUpgradeForm(data)

        assert not form.is_valid()
        assert len(form.errors) == 1
        assert "name" in form.errors
        assert form.errors["name"][0] == _("This field is required.")

    def test_organisation_validation_error_msg(self, user: User):
        """
        GIVEN an instance of UserUpgradeForm
        WHEN  posting form with no organisation
        THEN  should return error message
        """
        # The user already exists,
        # hence cannot be created.
        data = {
            "name": "some user",
            "organisation": None,
            "motivation": "blahblah",
        }
        form = UserUpgradeForm(data)

        assert not form.is_valid()
        assert len(form.errors) == 1
        assert "organisation" in form.errors
        assert form.errors["organisation"][0] == _("This field is required.")

    def test_motivation_validation_error_msg(self, user: User):
        """
        GIVEN an instance of UserUpgradeForm
        WHEN  posting form with blank motivation
        THEN  should return error message
        """
        # The user already exists,
        # hence cannot be created.
        data = {
            "name": user.name,
            "organisation": user.organisation,
            "motivation": "",
        }
        form = UserUpgradeForm(data)

        assert not form.is_valid()
        assert len(form.errors) == 1
        assert "motivation" in form.errors
        assert form.errors["motivation"][0] == _("This field is required.")

    def test_clean(self, user: User, rf: RequestFactory):
        """
        GIVEN
        WHEN
        THEN
        """
        data = {
            "name": user.name,
            "organisation": user.organisation,
            "motivation": "blahblah",
        }

        form = UserUpgradeForm(data)

        assert form.is_valid()

    @pytest.mark.skip(reason="test not implemented yet")
    def test_clean_fail(self):
        pass

    def test_update_user_name_success(self, user: User):
        """
        GIVEN a user (with no name)
        WHEN  filling the UpgradeForm with a user name
        THEN  update the database with this name
        """
        init = {
            "name": "",
            "organisation": user.organisation,
        }

        data = {
            "name": "another name",
            # organisation is a ForeignKey so we need to pass the object ID in data
            "organisation": user.organisation.pk,
            "motivation": "blahblah",
        }

        form = UserUpgradeForm(data, initial=init)
        # initiate `cleaned_data` attribute running `is_valid`
        form.is_valid()
        form.update_user(user)
        new = User.objects.get(id=user.id)

        assert form.is_valid()
        assert new.name == "another name"

    def test_update_user_name_error(self, user: User):
        """
        GIVEN a user (with a name)
        WHEN  filling the UpgradeForm with another name
        THEN  return an error
        """
        init = {
            "name": user.name,
            # "username": user.username,
            "organisation": user.organisation,
        }

        data = {
            "name": "another name",
            # organisation is a ForeignKey so we need to pass the object ID in data
            "organisation": user.organisation.pk,
            "motivation": "blahblah",
        }

        form = UserUpgradeForm(data, initial=init)
        # initiate `cleaned_data` attribute running `is_valid`
        form.is_valid()
        form.update_user(user)
        new = User.objects.get(id=user.id)

        assert new.name == user.name
        assert not form.is_valid()
        assert len(form.errors) == 1
        assert "name" in form.errors

    def test_update_user_organisation_error(self, user: User):
        """
        GIVEN a user (with an organisation)
        WHEN  filling the UpgradeForm with another organisation
        THEN  should return an error
        """
        init = {
            "name": user.name,
            # "username": user.username,
            "organisation": user.organisation,
        }

        data = {
            "name": user.name,
            "organisation": "another organisation",
            "motivation": "blahblah",
        }

        form = UserUpgradeForm(data, initial=init)
        # initiate `cleaned_data` attribute running `is_valid`
        form.is_valid()
        form.update_user(user)
        new = User.objects.get(id=user.id)

        assert new.organisation == user.organisation
        assert not form.is_valid()
        assert len(form.errors) == 1
        assert "organisation" in form.errors

    def test_update_user_organisation_success(
        self, user: User, organisation: Organisation
    ):
        """
        GIVEN a user (with no organisation)
        WHEN  filling the UpgradeForm with an organisation
        THEN  update the database with this name
        """
        init = {
            "name": user.name,
            # "username": user.username,
            "organisation": "",
        }

        data = {
            "name": user.name,
            # organisation is a ForeignKey so we need to pass the object ID in data
            "organisation": organisation.pk,
            "motivation": "blahblah",
        }

        form = UserUpgradeForm(data, initial=init)
        # initiate `cleaned_data` attribute running `is_valid`
        form.is_valid()
        form.update_user(user)
        new = User.objects.get(id=user.id)

        assert new.organisation == organisation
        assert form.is_valid()

    def test_send_email_error_message(self, user: User):
        """
        GIVEN a user
          And a filled UpgradeForm
          But no staff member
        WHEN  sending request to upgrade email
        THEN  should raise a ValueError
        """
        data = {
            "name": "some name",
            "organisation": "some organisation",
            "motivation": "some text\n maybe on several lines",
        }
        form = UserUpgradeForm(data)
        # initiate `cleaned_data` attribute running `is_valid`
        form.is_valid()

        with pytest.raises(ValueError, match="no recipient to who send email"):
            form.send_email(user)

    def test_send_email_success(
        self, user: User, staff: User, organisation: Organisation
    ):
        """
        GIVEN a user
          And a filled UpgradeForm
          And a staff member
        WHEN  sending request to upgrade email
        THEN  should return an error
        """
        data = {
            "name": "some name",
            "organisation": organisation.pk,
            "motivation": "some text\n maybe on several lines",
        }
        form = UserUpgradeForm(data)
        # initiate `cleaned_data` attribute running `is_valid`
        form.is_valid()
        form.send_email(user)

        # Now you can test delivery and email contents
        assert len(mail.outbox) == 1  # "Inbox is not empty"
        m = mail.outbox[0]
        assert m.subject == "Weahtervis: request to upgrade account"
        assert m.body.startswith("A user request to upgrade his permission.\n")
        assert form.cleaned_data.get("name") in m.body
        assert user.username in m.body
        assert form.cleaned_data.get("motivation") in m.body
        assert m.body.endswith(f"/admin/users/user/{user.id}/change/")
        assert m.from_email == settings.DEFAULT_FROM_EMAIL
        assert m.to == [staff.email]
