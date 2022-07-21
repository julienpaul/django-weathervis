# Stdlib imports
# Core Django imports
from django.contrib.gis.geos import Point, Polygon
from faker import Faker

# Third-party app imports
from faker.providers import BaseProvider

# Imports from my apps


class DjangoGeoPointProvider(BaseProvider):
    """
    based on https://stackoverflow.com/a/61059668
    """

    def geo_point(self, **kwargs):
        kwargs["coords_only"] = True
        # # generate() is not working in later Faker versions
        # faker = factory.Faker('local_latlng', **kwargs)
        # coords = faker.generate()
        fake = Faker()
        # coords: lat, lon
        coords = [float(x) for x in fake.latlng()]
        # coords: lon, lat
        coords.reverse()
        # coords: lon, lat, alt
        # coords.append(fake.pyfloat(positive=True, max_value=99999))
        coords.append(
            float(fake.pydecimal(right_digits=6, positive=True, max_value=99999))
        )
        return Point(*coords, srid=4326)


class DjangoGeoBBoxProvider(BaseProvider):
    """
    based on https://stackoverflow.com/a/61059668
    """

    def geo_bbox(self, **kwargs):
        kwargs["coords_only"] = True
        # # generate() is not working in later Faker versions
        # faker = factory.Faker('local_latlng', **kwargs)
        # coords = faker.generate()
        fake = Faker()
        # coords: lat, lon
        south, west = [float(x) for x in fake.latlng()]
        north, east = [float(x) for x in fake.latlng()]

        alt = float(fake.pydecimal(right_digits=6, positive=True, max_value=99999))

        coords = (
            (west, north, alt),
            (east, north, alt),
            (east, south, alt),
            (west, south, alt),
            (west, north, alt),
        )

        return Polygon(coords, srid=4326)
