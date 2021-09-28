# Stdlib imports
import pytest

# Core Django imports
from django.utils.translation import gettext_lazy as _

# Third-party app imports
# Imports from my apps
from src.organisations.forms import OrganisationForm
from src.organisations.models import Organisation

pytestmark = pytest.mark.django_db


class TestOrganisationForm:
    """
    Test class for all tests related to the OrganisationForm
    """

    def test_init_helper_layout(self):
        """
        GIVEN class OrganisationForm
        WHEN  initialised an instance
        THEN  instance should have attribute 'helper' and 'helper.layout'
        """
        form = OrganisationForm()
        assert hasattr(form, "helper")
        assert hasattr(form.helper, "layout")

    def test_name_validation_error_msg(self, organisation: Organisation):
        """
        Tests Organisation Form's unique validator functions correctly by testing:
            1) A new organisation with an existing name cannot be added.
            2) Only 1 error is raised by the Organisation Form
            3) The desired error message is raised
        """

        # The organisation already exists,
        # hence cannot be created.
        data = {
            "name": organisation.name,
        }
        form = OrganisationForm(data)

        assert not form.is_valid()
        assert len(form.errors) == 1
        assert "name" in form.errors
        assert form.errors["name"][0] == _(
            "An organisation with that name already exists."
        )

    def test_name_case_sensitive_validation_error_msg(self, organisation: Organisation):
        """
        Tests Organisation Form's unique validator functions correctly by testing:
            1) A new organisation with an existing name (but different case) cannot be added.
            2) Only 1 error is raised by the Organisation Form
            3) The desired error message is raised
        """
        # The user already exists,
        # hence cannot be created.
        data = {
            "name": organisation.name.upper(),
        }
        form = OrganisationForm(data)

        assert not form.is_valid()
        assert len(form.errors) == 1
        assert "name" in form.errors
        assert form.errors["name"][0] == _(
            "An organisation with that name already exists."
        )

        data = {
            "name": organisation.name.lower(),
        }
        form = OrganisationForm(data)

        assert not form.is_valid()
        assert len(form.errors) == 1
        assert "name" in form.errors
        assert form.errors["name"][0] == _(
            "An organisation with that name already exists."
        )

    @pytest.mark.skip(reason="test not implemented yet")
    def test_name_length_validation_error_msg(self, organisation: Organisation):
        pass

    @pytest.mark.skip(reason="test not implemented yet")
    def test_cripsy_form_inputs(self):
        """
        GIVEN class OrganisationForm with a cripsy form
        WHEN  displaying the layout through a view instance
        THEN  the inputs should appear on the view
        """
        pass

    @pytest.mark.skip(reason="test not implemented yet")
    def test_cripsy_form_buttons(self):
        """
        GIVEN class OrganisationForm with a cripsy form
        WHEN  displaying the layout through a view instance
        THEN  the buttons should appear on the view
        """
        pass

    @pytest.mark.skip(reason="test not implemented yet")
    def test_cripsy_form_redirect(self):
        """
        GIVEN class OrganisationForm with a cripsy form
        WHEN  clicking on the button display on the view
        THEN  should be redirect to
        """
        pass
