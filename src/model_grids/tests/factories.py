# Stdlib imports
# Core Django imports
from django.contrib.gis.geos import MultiPolygon, Polygon
from factory import Faker as FactoryFaker
from factory.django import DjangoModelFactory
from faker import Faker

# Third-party app imports
# Imports from my app
from src.model_grids.models import ModelGrid


class ModelGridFactory(DjangoModelFactory):
    class Meta:
        model = ModelGrid

    def _create_geom():
        """initialise a Polygon geometry"""
        fake = Faker()

        points_list = []
        for _ in range(3):
            # coords: lat, lon
            coords = [float(x) for x in fake.latlng()]
            # coords: lon, lat
            coords.reverse()
            # coords: lon, lat, alt
            coords.append(fake.pyfloat(positive=True, max_value=99999))
            points_list.append(coords)

        # add first point again, to close polygon
        points_list.append(points_list[0])

        return MultiPolygon(Polygon(points_list))

    name = FactoryFaker("company")
    geom = _create_geom()
