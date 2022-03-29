# Stdlib imports
# Core Django imports
# Third-party app imports
from factory import Faker as FactoryFaker
from factory import SubFactory, lazy_attribute
from factory.django import DjangoModelFactory

# Imports from my apps
from src.margins.tests.factories import MarginFactory
from src.stations.models import Station
from src.utils import util
from src.utils.tests.factories import DjangoGeoPointProvider


class StationFactory(DjangoModelFactory):
    class Meta:
        model = Station

    FactoryFaker.add_provider(DjangoGeoPointProvider)

    name = FactoryFaker("company")
    geom = FactoryFaker("geo_point")
    station_id = FactoryFaker("hexify", text="^^^^^^^^^^")
    wmo_id = FactoryFaker("hexify", text="^^^^^")
    description = FactoryFaker("sentence", nb_words=40)
    margin = SubFactory(MarginFactory)

    @lazy_attribute
    def margin_geom(self):
        return util.margin2polygon(
            self.geom.x,
            self.geom.y,
            self.geom.z,
            self.margin,
        )
