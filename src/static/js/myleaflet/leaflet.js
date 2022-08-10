/* variable specific. */
var map_leaflet;

/* method */
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
    // listen to event
    if (tag == 'domain') {
      // add Leaflet-Geoman controls with some options to the map
      add_geoman_control(map, tag)
      listen_domain(map) // need 'domain_url'
    } else if (tag == 'station') {
      // listen_pointer(map) // need 'station_url'
      listen_click(map) // need 'station_url'
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

  // save map
  map_leaflet = map;

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

function checkbox(bool) {
  if (bool) {
    return '<input class="form-check-input" type="checkbox" value="" disabled checked >'
  } else {
    return '<input class="form-check-input" type="checkbox" value="" disabled>'
  }
}

function listen_click(map) {
  // listen to 'click' on map
  map.on('click', function(e) {
    var popLocation= e.latlng;
    var popup = edit_station_popup(popLocation);
    popup.setLatLng(popLocation).openOn(map);
  });
}

function listen_pointer(map) {
  // listen to when a marker is created in Draw Mode
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
