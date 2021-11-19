# Stdlib import
import pytest

# Core Django imports
# Third-party app imports
# Imports from my apps
from src.stations.models import Station

pytestmark = pytest.mark.django_db


def test__str__(station: Station):
    """
    GIVEN an Station instance
    WHEN  printing the instance (without any attributes)
    THEN  return the station name
    """
    assert str(station) == f"{station.name}"


def test_longitude(station: Station):
    """
    GIVEN an Station instance s
    WHEN  looking for the s.longitude
    THEN  return the x attribute of geom
    """
    assert station.longitude == station.geom.x


def test_latitude(station: Station):
    """
    GIVEN an Station instance s
    WHEN  looking for the s.latitude
    THEN  return the y attribute of geom
    """
    assert station.latitude == station.geom.y


def test_altitude(station: Station):
    """
    GIVEN an Station instance s
    WHEN  looking for the s.altitude
    THEN  return the z attribute of geom
    """
    assert station.altitude == station.geom.z
