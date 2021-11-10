# Stdlib imports
# Core Django imports
from django.contrib.gis.geos import MultiPolygon, Polygon
from factory import Faker as FactoryFaker
from factory.django import DjangoModelFactory
from faker import Faker

# Third-party app imports
# Imports from my app
from src.weather_forecast.models import WeatherForecastBorder


class WeatherForecastBorderFactory(DjangoModelFactory):
    def _create_geom():
        """initialise a Polygon geometry"""
        fake = Faker()

        points_list = []
        for _ in range(3):
            points_list.append(fake.latlng())

        # add first point again, to close polygon
        points_list.append(points_list[0])

        return MultiPolygon(Polygon(points_list))

    name = FactoryFaker("company")
    geom = _create_geom()

    class Meta:
        model = WeatherForecastBorder
