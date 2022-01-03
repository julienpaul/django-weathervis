# Stdlib import
# Core Django imports
# Third-party app imports
import pytest

# Imports from my apps
from src.model_grids.models import ModelGrid

pytestmark = pytest.mark.django_db


def test__str__(modelGrid: ModelGrid):
    """
    GIVEN an ModelGrid instance
    WHEN  printing the instance (without any attributes)
    THEN  return the modelGrid name
    """
    assert str(modelGrid) == f"{modelGrid.name}, {modelGrid.date_valid_start}"
