# Stdlib import
import pytest

# Core Django imports
# Third-party app imports
# Imports from my apps
from src.margins.models import Margin
from src.utils.util import degree_sign as deg

pytestmark = pytest.mark.django_db


def test__str__(margin: Margin):
    """
    GIVEN an Margin instance
    WHEN  printing the instance (without any attributes)
    THEN  return the margin name
    """
    print(f"margin: {str(margin)}")
    assert (
        str(margin)
        == f"{margin.west}{deg}W | {margin.east}{deg}E | {margin.north}{deg}N | {margin.south}{deg}S"
    )
