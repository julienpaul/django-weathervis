# Stdlib imports
import pytest

# Core Django imports
# Third-party app imports
# Imports from my apps
from src.margins.forms import MarginForm
from src.margins.models import Margin


@pytest.mark.django_db
class TestMarginForm:
    """
    Test class for all tests related to the MarginForm
    """

    def test_init_helper_layout(self):
        """
        GIVEN class MarginForm
        WHEN  initialised an instance
        THEN  instance should have attribute 'helper' and 'helper.layout'
        """
        form = MarginForm()
        assert hasattr(form, "helper")
        assert hasattr(form.helper, "layout")

    def test_form_is_valid_raises_no_exception(self, margin: Margin):
        """
        GIVEN a MarginForm instance
        WHEN  adding a valid margin
        THEN  raise no Exception
        """
        data = {
            "east": 0.2,
            "west": 0.2,
            "north": 0.2,
            "south": 0.2,
        }
        form = MarginForm(data)

        try:
            form.is_valid()
        except Exception as exc:
            assert False, f"'form.is_valid()' raised an exception {exc}"
