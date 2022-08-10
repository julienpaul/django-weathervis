/* variable specific. */
var markers = {};
var clusters;

/* methods */
function set_station_popup(feature, map) {
  var popLocation= feature._latlng;

  var popup = edit_station_popup(popLocation);
  popup.setLatLng(popLocation).openOn(map);
}

function info_station_popup(feature) {
  if (document.getElementById('station_url') !== null) {

    var station_url = JSON.parse(document.getElementById('station_url').textContent);
    var _detail_url = station_url["station-detail"];
    // var _redirect_url = station_url["station-redirect"];

    var popup = L.popup().setContent(
      "<link rel='stylesheet' href='https://cdn.jsdelivr.net/npm/bootstrap-icons@1.5.0/font/bootstrap-icons.css'>\
      <div class='input-group mb-3'>\
      <dl>\
      <dt>Name</dt>\
      <dd><a class='btn btn-outline-primary btn-sm'\
       href=" + _detail_url.replace('dummy',feature.properties.slug) + " role='button'>\
       <i class='bi bi-eye'> "+feature.properties.name+"</i>\
       </a>\
      </dd>\
      <dt>Coordinates</dt>\
      <dd>("+
      feature.geometry.coordinates[0]+ String.fromCharCode(176) + "N, " +
      feature.geometry.coordinates[1] + String.fromCharCode(176) +"E)</dd>\
      <dt>Altitude</dt> <dd>"+feature.geometry.coordinates[2]+"m</dd>\
      <dt>\
      <div class='form-check'>"+checkbox(feature.properties.is_active)+"<label class='form-check-label' for='defaultCheck2'>is active</label></div>\
      </dt><dd></dd>\
      <dt>\
      <div class='form-check'>"+checkbox(feature.properties.uses_flexpart)+"<label class='form-check-label' for='defaultCheck2'>uses flexpart</label></div>\
      </dt><dd></dd>\
      </dl>"
      /*
      <a class='btn btn-outline-info btn-sm'\
       href=" + _redirect_url.replace('dummy',feature.properties.slug) + " role='button'>\
       <i class='bi bi-images'> plots</i>\
      </a>"
      */
    );
  } else {

    var popup = L.popup().setContent(feature.properties.name); // show popup with grid name

  }
  return popup
}

function edit_station_popup(feature) {
  if (document.getElementById('station_url') !== null) {

    let lat = feature.lat.toFixed(6)
    let lng = feature.lng.toFixed(6)

    // Generate URL without "id" bit
    // var _url = $("#station_url_id").attr("station-add");
    var station_url = JSON.parse(document.getElementById('station_url').textContent);
    var _url = station_url["station-add"];
    // If your expected result is "http://foo.bar/?x=1&y=2&x=42"
    var new_url = _url+'?latitude='+encodeURIComponent(lat)+'&longitude='+encodeURIComponent(lng)

    // Generate popup
    var popup = L.popup().setContent(
    "<link rel='stylesheet' href='https://cdn.jsdelivr.net/npm/bootstrap-icons@1.5.0/font/bootstrap-icons.css'>\
    <dl>\
    <dt>Coordinates</dt>\
    <dd>(" +
      lat + String.fromCharCode(176) + "N, " +
      lng + String.fromCharCode(176) + "E)</dd>\
    <dt><a class='btn btn-primary' href=" + new_url + " role='button'>\
    Add Station here</a></dt>\
    <dd></dd>\
    </dl>")

    return popup
  }
}

function style_icon(feature, tag) {
  var _marker
  var _icon = 'tint';
  var _prefix= 'fa';
  var _markerColor= 'blue';
  if (feature.properties.is_active) {
    switch (tag) {
      case 'local':
        _markerColor='green';
        break;
      default:
    }
  } else {
    _icon= 'umbrella';
    switch (tag) {
      case 'local':
        _markerColor='darkred';
        break;
      default:
        _markerColor='red';
    }
  }
  _marker = L.AwesomeMarkers.icon({
    icon: _icon,
    prefix: _prefix,
    markerColor: _markerColor,
  });
  return _marker
}

function add_pointers(map, controlLayers) {
  if (document.getElementById('station_data') !== null) {
    // see http://maptimeboston.github.io/leaflet-intro/
    var station_data = JSON.parse(document.getElementById('station_data').textContent);
    // var station_local = station_data["station-local"];
    var station_all_data = station_data["station-all"];
    var station_local = station_data["station-local"];

    var _lat=0
    var _lon=0
    // Download GeoJSON via Ajax
    $.getJSON(station_all_data, function (data) {
      // Add GeoJSON layer
      let stations = L.geoJson(data, {
        /*
        onEachFeature: function (feature, layer) {
          let popup = info_station_popup(feature);
          layer.bindPopup(popup);
        },
        */
        pointToLayer: function(feature,latlng){
          const _id = feature.properties.slug
          // customize icon
          let _icon
          if (_id == station_local) {
            _icon = style_icon(feature, 'local')
          } else {
            _icon = style_icon(feature)
          }
          markers[_id] = L.marker(
            latlng,
            {icon: _icon},
          ).setBouncingOptions({
            bounceHeight : 60,    // height of the bouncing
            bounceSpeed  : 40,    // bouncing speed coefficient
          });
          if (_id == station_local) {
            markers[_id].setZIndexOffset(100)
            let latlon = markers[_id].getLatLng()
            _lat = latlon.lat
            _lon = latlon.lng
          }
          let popup = info_station_popup(feature);
          markers[_id].bindPopup(popup).openPopup();
          return markers[_id];
        }
      });
      clusters = L.markerClusterGroup();

      clusters.addLayer(stations);
      map.addLayer(clusters);
        // Add 'stations' to Layer Control
        controlLayers.addOverlay(clusters, 'Stations');

    });
  }
}

/* show/hide flexpart parameters */
function HideFlexpart() {
  if(document.getElementById('id_uses_flexpart').checked == true) {
    document.getElementById('flexpart').style.display = '';
  } else {
    document.getElementById('flexpart').style.display = 'none';
  }
};

/* show/hide plots available */
function HidePlots() {
  if(document.getElementById('id_is_active').checked == true) {
    document.getElementById('plots').style.display = '';
  } else {
    document.getElementById('plots').style.display = 'none';
  }
};

// window.addEventListener('load', function () {
$(document).ready(function () {
  // listen to show/hide subcard

  // document.getElementById('list-bergen-list').tab('show');
  if(document.getElementById('id_uses_flexpart')) {
    HideFlexpart();
    document.getElementById('id_uses_flexpart').onchange = HideFlexpart;
  }

  if(document.getElementById('id_is_active')) {
    HidePlots();
    document.getElementById('id_is_active').onchange = HidePlots;
  }
})

function bounce_marker(slug) {
  m = markers[slug]
  // remove marker from markerClusterGroup
  clusters.removeLayer(m);
  // add marker to map
  map_leaflet.addLayer(m);
  // bounce three times
  m.bounce(3).on('bounceend',function() {
    // remove marker from map
    map_leaflet.removeLayer(m);
    // add marker to markerClusterGroup
    clusters.addLayer(m);
  });
}
