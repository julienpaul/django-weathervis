
function set_station_popup(feature, map) {
  var popLocation= feature._latlng;

  var popup = edit_station_popup(feature);
  popup.setLatLng(popLocation).openOn(map);
}

function info_station_popup(feature) {
  if (document.getElementById('station_url') !== null) {

    var station_url = JSON.parse(document.getElementById('station_url').textContent);
    var _detail_url = station_url["station-detail"];
    var _redirect_url = station_url["station-redirect"];

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
      <div class='form-check'>"+checkbox(feature)+"<label class='form-check-label' for='defaultCheck2'>is active</label></div>\
      </dt><dd></dd>\
      </dl>\
      <a class='btn btn-outline-info btn-sm'\
       href=" + _redirect_url.replace('dummy',feature.properties.slug) + " role='button'>\
       <i class='bi bi-images'> plots</i>\
      </a>"
    );
  } else {

    var popup = L.popup().setContent(feature.properties.name); // show popup with grid name

  }
  return popup
}

function edit_station_popup(feature) {
  if (document.getElementById('station_url') !== null) {

    let lat = feature._latlng.lat.toFixed(6)
    let lng = feature._latlng.lng.toFixed(6)

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
    var station_local = station_data["station-local"];
    var station_all_data = station_data["station-all"];
    // var station_local = $("#station_data_id").attr("station-local");
    // var station_all_data = $("#station_data_id").attr("station-all-geojson");
    var _lat=0
    var _lon=0
    // Download GeoJSON via Ajax
    $.getJSON(station_all_data, function (data) {
      // Add GeoJSON layer
      let stations = L.geoJson(data, {
        pointToLayer: function(feature,latlng){
          let _icon
          if (feature.properties.slug == station_local) {
            _icon = style_icon(feature, 'local')
          } else {
            _icon = style_icon(feature)
          }
          let marker = L.marker(
            latlng,
            {icon: _icon},
          );
          if (feature.properties.slug == station_local) {
            marker.setZIndexOffset(100)
            let latlon = marker.getLatLng()
            _lat = latlon.lat
            _lon = latlon.lng
          }
          let popup = info_station_popup(feature);
          marker.bindPopup(popup).openPopup();
          return marker;
        }
      });
      var clusters = L.markerClusterGroup();
      clusters.addLayer(stations);
      map.addLayer(clusters);
        // Add 'stations' to Layer Control
        controlLayers.addOverlay(clusters, 'Stations');
      // map.addLayer(stations);
      // Add 'stations' to Layer Control
      // controlLayers.addOverlay(stations, 'Local');
      // zoom on local
      // c1 = L.latLng(_lat - 0.1, _lon - 0.1);
      // c2 = L.latLng(_lat + 0.1, _lon + 0.1);
      // map.fitBounds(L.latLngBounds(c1, c2));
    });
  }
}
