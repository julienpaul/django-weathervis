
function main_map_init(map, options) {
  var controlLayers = map.layerscontrol;

  add_pointers(map, controlLayers)
  add_layers(map, controlLayers)

  click_pointer(map)

  /* ResetView see
  https://drustack.github.io/Leaflet.ResetView/#
  https://github.com/makinacorpus/django-leaflet/issues/39
  */
}

function local_map_init(map, options) {
  var controlLayers = map.layerscontrol;

  add_pointers(map, controlLayers)
  add_layer(map, controlLayers)
}

function checkbox(feature) {
  if (feature.properties.is_active) {
    return '<input class="form-check-input" type="checkbox" value="" disabled checked >'
  } else {
    return '<input class="form-check-input" type="checkbox" value="" disabled>'
  }
}

function click_pointer(map) {
  map.on('click', function(e) {
    var popLocation= e.latlng;
    let lat = e.latlng.lat.toFixed(6)
    let lng = e.latlng.lng.toFixed(6)
    // Generate URL without "id" bit
    // var _url = $("#station_url_id").attr("station-add");
    var station_url = JSON.parse(document.getElementById('station_url').textContent);
    var _url = station_url["station-add"];
    // If your expected result is "http://foo.bar/?x=1&y=2&x=42"
    var new_url = _url+'?latitude='+encodeURIComponent(lat)+'&longitude='+encodeURIComponent(lng)
    // Generate popup
    var _content =
    "<link rel='stylesheet' href='https://cdn.jsdelivr.net/npm/bootstrap-icons@1.5.0/font/bootstrap-icons.css'>\
    <dl>\
    <dt>Coordinates</dt>\
    <dd>(" +
      lat + String.fromCharCode(176) + "N, " +
      lng + String.fromCharCode(176) + "E)</dd>\
    <dt><a class='btn btn-primary' href=" + new_url + " role='button'>\
    Add Station here</a></dt>\
    <dd></dd>\
    </dl>"
    var popup = L.popup()
    .setLatLng(popLocation)
    .setContent(_content)
    .openOn(map);
  });
}

function pointer_popup(feature) {
  // var _url = $("#station_url_id").attr("station-detail");
  var station_url = JSON.parse(document.getElementById('station_url').textContent);
  var _detail_url = station_url["station-detail"];
  var _redirect_url = station_url["station-redirect"];
  let popup = L.popup().setContent(
    "<link rel='stylesheet' href='https://cdn.jsdelivr.net/npm/bootstrap-icons@1.5.0/font/bootstrap-icons.css'>\
    <div class='input-group mb-3'>\
    <dl>\
    <dt>Name</dt>\
    <dd><a class='btn btn-outline-primary btn-sm'\
     href=" + _detail_url.replace('dummy',feature.properties.name) + " role='button'>\
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
     href=" + _redirect_url.replace('dummy',feature.properties.name) + " role='button'>\
     <i class='bi bi-images'> plots</i>\
    </a>"
    );
  return popup
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
  // see http://maptimeboston.github.io/leaflet-intro/
  var station_data = JSON.parse(document.getElementById('station_data').textContent);
  console.log(station_data)
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
        let popup = pointer_popup(feature);
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
    c1 = L.latLng(_lat - 0.1, _lon - 0.1);
    c2 = L.latLng(_lat + 0.1, _lon + 0.1);
    // map.fitBounds(L.latLngBounds(c1, c2));
  });

}

function add_layer(map, controlLayers) {
  /* Add one polygon (margin) around local station */
  var station_data = JSON.parse(document.getElementById('station_data').textContent);
  console.log(station_data)
  var margin_local_data = station_data["margin_local"];
  // var grid_local_data = $("#station_data_id").attr("grid-local-geojson");
  // use zsh to hide layer at some zoom level
  zsh = new ZoomShowHide();
  zsh.addTo(map);
  $.getJSON(margin_local_data, function(data){
    // add GeoJSON layer to the map once the file is loaded
    let datalayers = L.geoJson(data ,{
      style: style_layer,
      onEachFeature: function(feature, layer) {
        // layer.on('mouseover', function () {
        layer.setStyle(style_layer(feature, 'local'));
        //   this.openPopup();
        // });
        // layer.on('mouseout', function () {
        //   this.setStyle(style_function());
        //   this.closePopup();
        // });
        layer.bindPopup(feature.properties.name);
        // Add 'layer' to Layer Control
        controlLayers.addOverlay(layer, feature.properties.name);
        layer.min_zoom = 6.5;
        zsh.addLayer(layer);
      },
    });
    map.fitBounds(datalayers.getBounds());
  });
}


function add_layers(map, controlLayers) {
  var grid_data = JSON.parse(document.getElementById('grid_data').textContent);
  var grid_all_data = grid_data["grid-all"];
  // var grid_all_data = $("#station_data_id").attr("grid-all-geojson");
  // use zsh to hide layer at some zoom level
  zsh = new ZoomShowHide();
  zsh.addTo(map);
  // read data from geojson
  $.getJSON(grid_all_data, function(data){
    // add GeoJSON layer to the map once the file is loaded
    var datalayers = L.geoJson(data ,{
      style: style_layer(),
      onEachFeature: function(feature, layer) {
        layer.on('mouseover', function () {
          this.setStyle(style_layer(feature, 'highlight'));
          // this.openPopup();
        });
        layer.on('mouseout', function () {
          this.setStyle(style_layer());
          // this.closePopup();
        });
        layer.bindPopup(feature.properties.name);
        // Add 'layer' to Layer Control
        controlLayers.addOverlay(layer, feature.properties.name);
        layer.max_zoom = 9.5;
        zsh.addLayer(layer);
      },
    });
    map.fitBounds(datalayers.getBounds());
  });
}

function style_layer(feature, tag) {
    var _fillColor = "#fff700";
    var _color = "white";
    var _weight = 1.5;
    var _dashArray = "5, 5";
    if (tag == 'highlight') {
        _color= "green";
        _weight= 2;
    } else if (tag == 'local') {
        _color= "red";
        _weight= 2;
    }

    return {
        "fillColor": _fillColor,
        "color": _color,
        "weight": _weight,
        "dashArray": _dashArray,
    };
  }
