
function map_station_list(map) { map_list(map, 'station') }
function map_station_local(map) { map_local(map, 'station') }
function map_station_edit(map) { map_edit(map, 'station') }
function map_station_local_edit(map) { map_local_edit(map, 'station') }

function map_domain_list(map) { map_list(map, 'domain') }
function map_domain_local(map) { map_local(map, 'domain') }
function map_domain_edit(map) { map_edit(map, 'domain') }
function map_domain_local_edit(map) { map_local_edit(map, 'domain') }

function map_list(map, tag) {
  map_init(map, tag, local=false, edit=false)
}

function map_local(map, tag) {
  map_init(map, tag, local=true, edit=false)
}

function map_edit(map, tag) {
  map_init(map, tag, local=false, edit=true)
}

function map_local_edit(map, tag) {
  map_init(map, tag, local=true, edit=true)
}

function map_init(map, tag, local=false, edit=false) {
  var controlLayers = map.layerscontrol;
  // Add mouse position control
  L.control.mousePosition({
    position:'bottomright',
    emptyString:'',
    lngFormatter: function(num) {
      var direction = 'E';
      if (num > 180) {
        var lng = num - 360
      } else if (num < -180) {
        var lng = num + 360
      } else {
        var lng = num
      }
      var formatted = L.Util.formatNum(lng, 6) + 'º ' + direction;
      return formatted;
    },
    latFormatter: function(num) {
      var direction = 'N';
      var formatted = L.Util.formatNum(num, 6) + 'º ' + direction;
      return formatted;
    }
  }).addTo(map);

  if (edit) {
    // add Leaflet-Geoman controls with some options to the map
    add_geoman_control(map, tag)
    // listen to event
    if (tag == 'domain') {
      listen_domain(map) // need 'domain_url'
    } else if (tag == 'station') {
      listen_pointer(map) // need 'station_url'
    }
  }
  add_pointers(map, controlLayers) // need 'station_data'

  if (local) {
    add_layer(map, controlLayers, 'station') // need 'station_data'
    add_layer(map, controlLayers, 'domain') // need 'domain_data'
  } else {
    add_layers(map, controlLayers, 'grid') // need 'grid_data'
    add_layers(map, controlLayers, 'domain') // need 'domain_data'
  }

  /* ResetView see
  https://drustack.github.io/Leaflet.ResetView/#
  https://github.com/makinacorpus/django-leaflet/issues/39
  */
}

function add_geoman_control(map, tag) {
  // add Leaflet-Geoman controls with some options to the map
  var hash = { position: 'topleft',
    drawMarker: false,
    drawCircleMarker: false,
    drawPolyline: false,
    drawRectangle: false,
    drawCircle: false,
    drawPolygon: false,
    oneBlock: false,
    drawText: false,
    editMode:	true,
    dragMode:	true,
    cutPolygon: false,
    removalMode:	true,
    rotateMode: false,
  };

  if (tag == 'domain') {
    hash['drawRectangle'] = true;
  } else if (tag == 'station') {
    hash['drawMarker'] = true;
  }

  map.pm.addControls(hash);
}

function checkbox(feature) {
  if (feature.properties.is_active) {
    return '<input class="form-check-input" type="checkbox" value="" disabled checked >'
  } else {
    return '<input class="form-check-input" type="checkbox" value="" disabled>'
  }
}

function listen_pointer(map) {
  map.on('pm:create', function(e) {
    marker = e.marker
    set_station_popup(marker, map)
    // listen to when a marker is changed in Edit Mode
    marker.on('pm:update', function(e) {
      set_station_popup(marker, map)
    });
    // disable drawing second marker
    map.pm.enableDraw('Marker', {
      continueDrawing: false
    });
  });
}

function listen_domain(map) {
  // listen to when a layer is created in Draw Mode
  map.on('pm:create', function (e) {
    layer = e.layer
    set_domain_popup(layer, map)
    // listen to when a layer is changed in Edit Mode
    layer.on('pm:update', function(e) {
      set_domain_popup(layer, map)
    });

  });
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

function add_pointers(map, controlLayers) {
  if (document.getElementById('station_data') !== null) {
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

function add_layer(map, controlLayers, tag) {
  if (tag == 'station') {
    _id = 'station_data'
    _local = 'margin_local'
    _url = 'no_url'
    _zoom_min = 6.5
  } else if (tag == 'domain') {
    _id = 'domain_data'
    _local = 'domain-local'
    _url = 'domain_url'
    _zoom_min = 1
  } else {
    _id = 'no_data'
    _url = 'no_url'
  }
  console.log('toto')
  if (document.getElementById(_id) !== null) {
    /* Add one polygon (margin) around local station */
    var dic_data = JSON.parse(document.getElementById(_id).textContent);
    var local_data = dic_data[_local];
    console.log(local_data)
    // var grid_local_data = $("#station_data_id").attr("grid-local-geojson");
    // use zsh to hide layer at some zoom level
    zsh = new ZoomShowHide();
    zsh.addTo(map);
    $.getJSON(local_data, function(data){
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
          console.log(layer)
          if (document.getElementById(_url) !== null) {
            let popup = info_domain_popup(feature);
            layer.bindPopup(popup).openPopup();
          } else {
            layer.bindPopup(feature.properties.name); // show popup with grid name
          }
          // Add 'layer' to Layer Control
          controlLayers.addOverlay(layer, feature.properties.name);
          // hide layer at some zoom level
          layer.min_zoom = _zoom_min;
          zsh.addLayer(layer);
        },
      });
      map.fitBounds(datalayers.getBounds());
      console.log(datalayers)
    });
  }
}

function add_layers(map, controlLayers, tag) {
  if (tag == 'grid') {
    _id = 'grid_data'
    _all = 'grid-all'
    _url = 'no_url'
  } else if (tag == 'domain') {
    _id = 'domain_data'
    _all = 'domain-all'
    _url = 'domain_url'
  } else {
    _id = 'no_data'
    _url = 'no_url'
  }
  if (document.getElementById(_id) !== null) {
    var dic_data = JSON.parse(document.getElementById(_id).textContent);
    var all_data = dic_data[_all];
    // var grid_all_data = $("#station_data_id").attr("grid-all-geojson");
    // use zsh to hide layer at some zoom level
    zsh = new ZoomShowHide();
    zsh.addTo(map);
    // read data from geojson
    $.getJSON(all_data, function(data){
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
          if (tag == 'domain') {
            if (document.getElementById(_url) !== null) {
              let popup = info_domain_popup(feature);
              layer.bindPopup(popup).openPopup();
              // layer.bindPopup(popup).openPopup();
            } else {
              layer.bindPopup(feature.properties.name); // show popup with grid name
            }
          }
          // Add 'layer' to Layer Control
          controlLayers.addOverlay(layer, feature.properties.name);
          // layer ignored by Leaflet-Geoman
          layer.setStyle({pmIgnore: true});
          // hide layer at some zoom level
          layer.max_zoom = 9.5;
          zsh.addLayer(layer);
        },
      });
      map.fitBounds(datalayers.getBounds());
    });
  }
}
