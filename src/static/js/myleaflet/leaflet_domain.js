
function set_domain_popup(feature, map) {

  var southWest = feature._bounds._southWest;
  var northEast = feature._bounds._northEast;

  var popLocation= L.PM.Utils.calcMiddleLatLng(map, southWest, northEast);

  var popup = edit_domain_popup(feature)
  popup.setLatLng(popLocation).openOn(map);
}

function info_domain_popup(feature) {
  if (document.getElementById('domain_url') !== null) {

    var domain_url = JSON.parse(document.getElementById('domain_url').textContent);
    var _detail_url = domain_url["domain-detail"];
    var _redirect_url = domain_url["domain-redirect"];

    var lat_sw = feature.geometry.coordinates[0][0][0].toFixed(6);
    var lng_sw = feature.geometry.coordinates[0][0][1].toFixed(6);
    var lat_ne = feature.geometry.coordinates[0][2][0].toFixed(6);
    var lng_ne = feature.geometry.coordinates[0][2][1].toFixed(6);
    var alt = feature.geometry.coordinates[0][0][2];

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
      <dt>Bounding Box</dt>\
      <dd>[" +
        lat_sw + String.fromCharCode(176) + "N, " +
        lat_ne + String.fromCharCode(176) + "N, " +
        lng_sw + String.fromCharCode(176) + "E, " +
        lng_ne + String.fromCharCode(176) + "E]</dd>\
      <dt>Altitude</dt> <dd>"+alt+"m</dd>\
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

function edit_domain_popup(feature) {
  if (document.getElementById('domain_url') !== null) {

    var southWest = feature._bounds._southWest;
    var northEast = feature._bounds._northEast;

    // var popLocation= L.PM.Utils.calcMiddleLatLng(map, southWest, northEast);

    var lat_sw = southWest.lat.toFixed(6);
    var lng_sw = southWest.lng.toFixed(6);
    var lat_ne = northEast.lat.toFixed(6);
    var lng_ne = northEast.lng.toFixed(6);

    // Generate URL without "id" bit
    // var _url = $("#station_url_id").attr("station-add");
    var domain_url = JSON.parse(document.getElementById('domain_url').textContent);
    var _url = domain_url["domain-add"];
    // If your expected result is "http://foo.bar/?x=1&y=2&x=42"
    var new_url = _url + '?bbox=' + encodeURIComponent(lng_sw) +
     '&bbox=' + encodeURIComponent(lat_ne) +
     '&bbox=' + encodeURIComponent(lng_ne) +
     '&bbox=' + encodeURIComponent(lat_sw)

    // Generate popup
    var popup = L.popup().setContent(
      "<link rel='stylesheet' href='https://cdn.jsdelivr.net/npm/bootstrap-icons@1.5.0/font/bootstrap-icons.css'>\
      <dl>\
      <dt>Bounding Box</dt>\
      <dd>[" +
        lat_sw + String.fromCharCode(176) + "N, " +
        lat_ne + String.fromCharCode(176) + "N, " +
        lng_sw + String.fromCharCode(176) + "E, " +
        lng_ne + String.fromCharCode(176) + "E]</dd>\
      <dt><a class='btn btn-primary' href=" + new_url + " role='button'>\
      Add Domain here</a></dt>\
      <dd></dd>\
      </dl>"
    );
    return popup
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
  if (document.getElementById(_id) !== null) {
    /* Add one polygon (margin) around local station */
    var dic_data = JSON.parse(document.getElementById(_id).textContent);
    var local_data = dic_data[_local];
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
