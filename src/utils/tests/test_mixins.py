# Stdlib imports
# Core Django imports
from crispy_forms.layout import Layout

# Third-party app imports
# Imports from my apps
from src.utils.mixins import CrispyMixin


class TestCrispyMixin:
    """
    Test class for all tests related to the CrispyMixin
    """

    class DummyForm(CrispyMixin):
        pass

    def test_init_helper_layout(self):
        """
        GIVEN class UserUpdateForm
        WHEN  initialised an instance
        THEN  instance should have attribute 'helper'
          and an attribute 'helper.layout'
        """
        form = self.DummyForm()
        assert hasattr(form, "helper")
        assert hasattr(form.helper, "layout")
        assert isinstance(form.helper.layout, Layout)
