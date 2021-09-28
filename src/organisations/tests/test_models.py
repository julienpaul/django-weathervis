# Stdlib import
import pytest

# Core Django imports
# Third-party app imports
# Imports from my apps
from src.organisations.models import Organisation

pytestmark = pytest.mark.django_db


def test__str__(organisation: Organisation):
    """
    GIVEN an Organisation instance
    WHEN  printing the instance (without any attributes)
    THEN  return the organisation name
    """
    assert str(organisation) == f"{organisation.name}"
