# Stdlib imports
# Core Django import
# Third-party app imports
import folium
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from django.urls import reverse_lazy
from folium.plugins import MarkerCluster, MiniMap, MousePosition

# Imports from my app
from src.model_grids.models import ModelGrid
from src.stations.models import Station
from src.utils.util import degree_sign as deg

# TODO LogoutIfNotStaffMixin
# see https://stackoverflow.com/questions/44341391/django-class-based-view-logout-user-if-not-staff


class SuccessURLAllowedHostsMixin:
    success_url_allowed_hosts = set()

    def get_success_url_allowed_hosts(self):
        return {self.request.get_host(), *self.success_url_allowed_hosts}


class CrispyMixin:
    class Meta:
        fields = ""
        # fields = ("name", "organisation", "motivation")
        # hide = ("username", "bio")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # init crispy helper
        self.helper = FormHelper()
        self._init_helper_layout()
        # customize it
        self._custom_helper()

    def _init_helper_layout(self):
        """initialise crispy layout"""
        self.helper.layout = Layout(
            # ButtonHolder(
            #     Submit("submit", "Submit", css_class="btn-success"),
            #     Button(
            #         "cancel",
            #         "Cancel",
            #         css_class="btn-primary",
            #         onclick="history.go(-1);",
            #     ),
        )

    def _custom_helper(self):
        """customize crispy form"""
        pass
        # for field in self.fields: # self.Meta.hide:
        #     self.helper[field].update_attributes(hidden=True)
        #     self.helper.layout.insert(-1, Field(field))


class DrawMapMixin:
    """[draw map with markers]

    Returns:
        [type]: [description]
    """

    # Available background:
    # OpenStreetMap
    # Stamen Terrain
    # Stamen Toner
    # Stamen Watercolor
    # Cartodb Positron
    # Cartodb dark_matter
    _tiles = "OpenStreetMap"

    # TODO create similar class with ipyleaflet
    # The interactive functionality in IpyLeaflet is unparalleled
    # as Widgets enable bidirectional interactions. Therefore,
    # your maps are not only interactive but also can capture user
    # inputs to trigger new computations.

    # Bergen/Coordinates
    # 60.3913° N, 5.3221° E
    # Stavanger/Coordinates
    # 58.9700° N, 5.7331° E
    # Haugesund/Coordinates
    # 59.4136° N, 5.2680° E
    # Oslo/Coordinates
    # 59.9139° N, 10.7522° E
    # Osøyro/Coordinates
    # 60.1839° N, 5.4638° E
    # Kristiansand/Coordinates
    # 58.1599° N, 8.0182° E
    # Paris/Coordinates
    # 48.8566° N, 2.3522° E

    def _init_map(self, local: Station = None):
        # Bergen ip adress
        # ip = "129.177.11.27"
        # centroid = forecasts.geom.centroid
        # TODO compute initial position
        # _= []
        # for f in self.forecasts:
        #    _.append([p.x, p.y for p in f.geom.centroid])

        # default
        lat, lon = 60.3913, 5.3221
        _zoom_start = 5
        if local is not None:
            if isinstance(local, Station):
                lat, lon = local.latitude, local.longitude
                _zoom_start = 8
            else:
                raise TypeError("Invalid type. Argument 'local' must be a Station")
        # initial folium map
        mapobj = folium.Map(
            # width=800,
            # height=500,
            location=(lat, lon),
            zoom_start=_zoom_start,
            tiles=self._tiles,
        )
        degree_north = "function(num) {return L.Util.formatNum(num, 4) + ' º N';};"
        degree_east = "function(num) {return L.Util.formatNum(num, 4) + ' º E';};"

        MousePosition(
            position="bottomleft",
            separator=" | ",
            empty_string="NaN",
            lng_first=True,
            num_digits=20,
            prefix="Coordinates:",
            lat_formatter=degree_north,
            lng_formatter=degree_east,
        ).add_to(mapobj)

        return mapobj

    def _add_minmap(self, mapobj):
        minimap = MiniMap(
            position="bottomright",
            toggle_display=True,
            tile_layer=self._tiles,
            # width=200,
            # height=100,
        )
        mapobj.add_child(minimap)

        return mapobj

    def _add_polygon(self, mapobj: folium.Map, pnt: Station, color="blue"):
        def style_function(feature):
            return {
                "fillColor": "#ffaf00",
                "color": color,
                "weight": 1.5,
                "dashArray": "5, 5",
            }

        def highlight_function(feature):
            return {
                "fillColor": "#ffaf00",
                "color": "green",
                "weight": 3,
                "dashArray": "5, 5",
            }

        poly = pnt.margin_geom
        geo_j = folium.GeoJson(
            data=poly.geojson,
            name=("margin around station: {}".format(pnt.name)),
            style_function=style_function,
            highlight_function=highlight_function,
        )
        folium.Popup(f"margin around {pnt.name}").add_to(geo_j)
        geo_j.add_to(mapobj)

        return mapobj

    def _add_forecast(self, mapobj: folium.Map):
        def style_function(feature):
            return {
                "fillColor": "#ffaf00",
                "color": "blue",
                "weight": 1.5,
                "dashArray": "5, 5",
            }

        def highlight_function(feature):
            return {
                "fillColor": "#ffaf00",
                "color": "green",
                "weight": 3,
                "dashArray": "5, 5",
            }

        forecats = ModelGrid.objects.all()
        for forecast in forecats:
            poly = forecast.geom
            geo_j = folium.GeoJson(
                data=poly.geojson,
                name=("forecast: {}".format(forecast.name)),
                style_function=style_function,
                highlight_function=highlight_function,
            )
            folium.Popup(forecast.name).add_to(geo_j)
            geo_j.add_to(mapobj)

        return mapobj

    def _get_popup(self, station_):
        """filled popup"""
        checkbox = '<input class="form-check-input" type="checkbox" value="" disabled checked >'
        if not station_.is_active:
            checkbox = (
                '<input class="form-check-input" type="checkbox" value="" disabled>'
            )
        html = f"""
                <link rel="stylesheet"
                    href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.5.0/font/bootstrap-icons.css">
                <dl>
                   <dt>Name</dt>
                   <dd>{station_.name}</dd>
                   <dt>Coordinates</dt>
                   <dd>({station_.latitude}{deg}N,{station_.longitude}{deg}E)</dd>
                   <dt>Altitude</dt>
                   <dd>{station_.altitude}m</dd>
                 </dl>
                 <div class="form-check">
                    {checkbox}
                   <label class="form-check-label" for="defaultCheck2">
                     is active
                   </label>
                 </div>
                <!--
                <div class="input-group mb-3">
                    <div class="input-group-append">
                        <a class="btn btn-primary"
                           href="{reverse_lazy("stations:detail", kwargs={"slug": station_.slug})}"
                           role="button">
                        <i class="bi bi-eye"></i>
                    </a>
                    <a class="btn btn-success"
                       href="{reverse_lazy("stations:update", kwargs={"slug": station_.slug})}"
                       role="button">
                        <i class="bi bi-pencil"></i>
                    </a>
                   </div>
                 </div>
                 -->
                """
        return html

    def _add_marker(self, mapobj: folium.Map, pnt: Station, color="blue"):
        _zoffset = int(pnt.latitude)
        if color != "blue":
            _zoffset = 100
            if not pnt.is_active:
                color = "darkred"
        html = self._get_popup(pnt)
        folium.Marker(
            [pnt.latitude, pnt.longitude],
            z_index_offset=_zoffset,
            tooltip="Click me!",
            popup=html,
            icon=folium.Icon(color=color, icon="home", prefix="fa"),
        ).add_to(mapobj)

        return mapobj

    def _add_points(self, mapobj: folium.Map, local: Station = None):
        # Create empty lists to contain the point coordinates and the point pop-up information
        coords, popups, icons = [], [], []
        for pnt in Station.objects.all():
            if pnt != local:
                color = "blue"
                if not pnt.is_active:
                    color = "cadetblue"
                # Append lat and long coordinates to "coords" list
                coords.append([pnt.latitude, pnt.longitude])
                html = self._get_popup(pnt)
                popups.append(html)

                icon = folium.Icon(color=color, icon="cloud", prefix="fa")
                icons.append(icon)

        # Create a Folium feature group for this layer, since we will be displaying multiple layers
        pt_lyr = folium.FeatureGroup(name="stations")
        if coords:
            # Add the clustered points of crime locations and popups to this layer
            pt_lyr.add_child(
                MarkerCluster(locations=coords, popups=popups, icons=icons)
            )
            # Add this point layer to the map object
            mapobj.add_child(pt_lyr)

        if local:
            mapobj = self._add_marker(mapobj, local, color="red")
            mapobj = self._add_polygon(mapobj, local, color="red")

        return mapobj

    def draw_map(self, local: Station = None):
        # create map
        m = self._init_map(local)
        # overlay forecast model domain
        m = self._add_forecast(m)
        # overlay points
        m = self._add_points(m, local)
        # overlay minimap
        m = self._add_minmap(m)
        # overlay layer control
        folium.LayerControl().add_to(m)
        return m
