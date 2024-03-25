var id_city = document.getElementById('id_city')
var id_context = document.getElementById('id_context')
var id_time_zone = document.getElementById('id_time_zone')
var id_latitude = document.getElementById('id_latitude')
var id_longitude = document.getElementById('id_longitude')

oMap = function() {

  data = {};
  degree_precision = 0.01;
  max_viapoints = 50;
  var latlng;
  var marker;

  pointLocation=Array();
  pk_point_location=1;

  var self = this;
  this.init = function(elemId, init_latlon) {

    self.initMap(elemId);
    self.initOpenStreetLayer();
    // self.initLegendControlLayer();
    self.update_view(init_latlon[0], init_latlon[1]);
//     var zoom = 6;
//     Window.map.setView(new L.LatLng(init_latlon[0], init_latlon[1]), zoom);
    // nextmarkertype = true;
    Window.map.on('click', onMapClick);
  };
  this.initMap = function(elemId) {
    Window.map = L.map(elemId, {
      preferCanvas: true,
      fullscreenControl: true
    });
  };

  this.initOpenStreetLayer = function() {
    // create the tile layer with correct attribution
    // map provider list => http://leaflet-extras.github.io/leaflet-providers/preview/
    var osmUrl = "http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png";
    var osmAttrib =
      '&copy; <a href="http://openstreetmap.org/copyright">OpenStreetMap</a> contributors';
    self.osmLayer = new L.TileLayer(osmUrl, {
      minZoom: 1,
      maxZoom: 12,
      updateWhenZooming: false,      // map wont update tiles until zoom is done
      updateWhenIdle: true,          // map wont load new tiles when panning
      attribution: osmAttrib
    });
    self.osmLayer.addTo(Window.map);

  };
  this.addLayer = function(layer) {
    return Window.map.addLayer(layer);
  };
  this.getOSMLayer = function() {
    return self.osmLayer;
  };
  this.getMap = function() {
    return Window.map;
  };
  this.update_view = function(lat, lon) {
    var zoom = 9;
    Window.map.setView(new L.LatLng(lat, lon), zoom);
  }
//  this.initLegendControlLayer = function(container, content) {
//    self.legendControlLayer = L.control({ position: "bottomright" });
//    self.legendControlLayer.onAdd = function(map) {
//      var div = L.DomUtil.create(
//        "div",
//        "info_legend",
//        document.getElementById(container)
//      );
//      div.innerHTML += content;
//      div.setAttribute("id", "legend");
//      return div;
//    };
//    self.legendControlLayer.addTo(Window.map);
//  };

//    this.updateLegendControlLayer = function(content) {
//       var div = document.getElementById("legend");
//       div.innerHTML = content;
//  };
}

oMap.prototype.constructor = oMap;

var omap;

function create_map(latitude, longitude) {

      var init_latlon = [ latitude, longitude];

      omap = new oMap();

      omap.init("map", init_latlon);

      update_marker_on_map(latitude, longitude)
}

function get_icon(color) {

    var iconUrl;

    if (color == 'green') {
        iconUrl = "../../static/leaflet/images/marker-icon-green3.png";
        }

    else if (color == 'red') {
        iconUrl = "../../static/leaflet/images/marker-icon-red.png";
    } else {
        iconUrl = "../../static/leaflet/images/marker-icon.png";
    }
    appIcon = L.Icon.Default.extend({
        options: {
            iconUrl: iconUrl,
            shadowUrl: '../../static/leaflet/images/marker-shadow.png'
        }
        });

        var icon = new appIcon();
        return icon;
}

function onDragEndMarker() {

   this.update();
}

function onPopupOpen() {
	var tempMarker = this
  alert(tempMarker);
    // To remove marker on click of delete
    $(".marker-delete-button:visible").click(function () {
		removeMarker(tempMarker);
    });
}

function removeLocation(pk) {

	for(i=0;i<pointLocation.length;i++) {
	    var locationi = pointLocation[i.toString()];
		if (locationi.pk === pk) {
		   pointLocation.splice(i, 1);
		   break;
		   }
	    }

}
function removeMarker(marker) {

    Window.map.removeLayer(marker);
    removeLocation(marker.pk_point_location);
    //markers.splice(markers.indexOf(marker), 1);
    //delete marker;
}

function addMarker(markerLocation) {

    var icon = get_icon("red");

    var marker = new L.Marker(markerLocation,
		{ icon: icon,
                  riseOnHover: true,
                  draggable: true
		}).bindPopup("<input type='button' value='Lieu de naissance' class='marker-delete-button' submit=''/>");

    marker.addTo(Window.map);
    return marker;


}



function validerDefinitionTheme(event) {
  var date = document.getElementById('datetime').value
  displayTheme(date, Window.map.latlng);
}

function addLocation(marker, zlatlng) {

    var newLocation = new PointLocation(pk_point_location, marker, zlatlng);
    pointLocation.push(newLocation);
    current_pk = pk_point_location;
    // add 1 to the pk_point_location to prepare next marker creation
	pk_point_location = pk_point_location + 1;
	return current_pk;
}

function format_latlng(lat, lng) {

		var data = {'coordinate':[lat.toFixed(5), lng.toFixed(5)]};
		return data;
}

function latlon_precision(x) {
  return Number.parseFloat(x).toPrecision(8);
}

//function update_map(lat, lng, location, timezone, country_index, countries) {
function update_marker_on_map(lat, lng) {

    var formatted_latlng = format_latlng(lat, lng)

    var coord = L.latLng(lat, lng);

    omap.update_view(lat, lng);

    // eliminate non-coherent response
    if (Math.abs(lat - formatted_latlng.coordinate[0]) > self.degree_precision ||
            Math.abs(lng - formatted_latlng.coordinate[1]) > self.degree_precision) {
        return;
    }

    if (Window.map.marker != null) {
      Window.map.removeLayer(Window.map.marker);
    }

    var nearest_coord = L.latLng(
       formatted_latlng.coordinate[0],
       formatted_latlng.coordinate[1]
    );

	Window.map.marker = addMarker(nearest_coord);

   // form inputs updating

//    document.getElementById('id_latitude').value = lat;
//    document.getElementById('id_longitude').value = lng;

}

function onMapClick(e) {

    var lat = latlon_precision(e.latlng.lat);
    var lng = latlon_precision(e.latlng.lng);
alert(lat);
alert(lng);
    document.getElementById('id_latitude').value = lat ;
    document.getElementById('id_longitude').value = lng ;

    update_french_city_name_and_context(lat, lng);
    update_new_city(lat, lng);

}

function update_new_city(latitude, longitude) {

    update_marker_on_map(latitude, longitude);

    update_city_data_from_geoname_webservice();

}
////--------------------------------------------------
//function update_marker_on_map(lat, lon) {
////--------------------------------------------------
//  var xmlhttp = new XMLHttpRequest();
//  xmlhttp.onreadystatechange = function() {
//    if (this.readyState == 4 && this.status == 200) {
//
//        var data = JSON.parse(xmlhttp.responseText);
//           // inputs updatings
//
////        update_map(data.latitude, data.longitude, data.city, data.timezone, data.country_index, data.countries)
//        update_map(data.latitude, data.longitude, data.city, data.time_zone)
//
//    }
//  };
////  var uri = "location/?lat=" + lat + "&lon=" + lon
//  var uri = "timezone"
//  const encoded = encodeURI(uri);
//  xmlhttp.open("POST", encoded, true);
//  xmlhttp.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
//  xmlhttp.setRequestHeader('X-CSRF-TOKEN', '<YOURTOKENHERE>');
//  xmlhttp.send('latitude=' + lat + '&longitude=' + lon);
//
//
//}

function save_theme() {

var form = '#id-new-theme-form';

$.ajax({
    url: "{% url 'save_theme' %}",
    type: "POST",
    data: $(form).serialize(),
    success: function(data) {
        if (!(data['success'])) {
            $(form).replaceWith(data['form_html']);
        }
        else {
            // Here you can show the user a success message or do whatever you need
            $(form).find('.success-message').show();
        }
    },
    error: function () {
        $(form).find('.error-message').show()
    }
});


}


function add_city_selector_listener(ids) {
  /*the autocomplete function takes two arguments,
  the text field element and an array of possible autocompleted values:*/
  var currentFocus;
  /*execute a function when someone writes in the text field:*/
  ids['city'].addEventListener("input", function(e) {
      var a, b, i, val = this.value;
      /*close any already open lists of autocompleted values*/
      closeAllLists();
      if (!val) { return false;}

      var xmlhttp = new XMLHttpRequest()

      var input_element = this;

      xmlhttp.onreadystatechange = function() {

          if (this.readyState == 4 && (this.status == 200 || this.status == 0)) {
              var data =  JSON.parse(xmlhttp.responseText);

              currentFocus = -1;
              /*create a DIV element that will contain the items (values):*/
              a = document.createElement("DIV");
              a.setAttribute("id", input_element.id + "cities-list");
              a.setAttribute("class", "cities-items");
              /*append the DIV element as a child of the autocomplete container:*/
              input_element.parentNode.appendChild(a);
              /*for each item in the array...*/
              for (var i = 0; i < data.features.length; i++) {
                var feature = data.features[i];
                var label = feature.properties.label
                var context = feature.properties.context
                /*check if the item starts with the same letters as the text field value:*/
                if (label.substr(0, val.length).toUpperCase() == val.toUpperCase()) {
                  /*create a DIV element for each matching element:*/
                  b = document.createElement("DIV");
                  /*make the matching letters bold:*/
                  b.innerHTML = "<strong>" + label + "</strong>";
                  b.innerHTML += "<br>";
                  b.innerHTML += context;
                  /*insert a input field that will hold the current array item's value:*/
                  b.innerHTML += "<input id='city-name' type='hidden' value='" + label + "'>";
                  b.innerHTML += "<input id='city-latitude' type='hidden' value='" + feature.geometry.coordinates[1] + "'>";
                  b.innerHTML += "<input id='city-longitude' type='hidden' value='" + feature.geometry.coordinates[0] + "'>";
                  b.innerHTML += '<input id="city-context" type="hidden" maxlength="120" value="' + context + '">';
                  /*execute a function when someone clicks on the item value (DIV element):*/

                  b.addEventListener("click", function(e) {
                      /*insert the value for the autocomplete text field:*/
                      ids['city'].value = this.getElementsByTagName("input")[0].value;
                      var str_latitude = this.getElementsByTagName("input")[1].value;
                      var latitude = parseFloat(str_latitude);
                      ids['latitude'].value = latitude;
//                      ids['latitude'].onchange();

                      var str_longitude = this.getElementsByTagName("input")[2].value;
                      var longitude = parseFloat(str_longitude);
                      ids['longitude'].value = longitude;

                      var context = this.getElementsByTagName("input")[3].value;
                      console.log(context);
                      ids['context'].value = context;
//                      ids['longitude'].onchange();

                      update_new_city(latitude, longitude);
                      /*close the list of autocompleted values,
                      (or any other open lists of autocompleted values:*/
                      closeAllLists();
                  });
                  a.appendChild(b);
                }
              }

      		} else if (this.readyState < 4) {
      			// document.getElementById("loader").style.display = "inline";
      		}
      };

      var q = encodeURIComponent(val);

      var uri = 'https://api-adresse.data.gouv.fr/search/?q=' + q + '&type=municipality&autocomplete=1';
      const encoded = encodeURI(uri);

      xmlhttp.open("GET", encoded);

      xmlhttp.send(null);

  });
  /*execute a function presses a key on the keyboard:*/
  ids['city'].addEventListener("keydown", function(e) {
      var x = document.getElementById(this.id + "cities-list");
      if (x) x = x.getElementsByTagName("div");
      if (e.keyCode == 40) {
        /*If the arrow DOWN key is pressed,
        increase the currentFocus variable:*/
        currentFocus++;
        /*and and make the current item more visible:*/
        addActive(x);
      } else if (e.keyCode == 38) { //up
        /*If the arrow UP key is pressed,
        decrease the currentFocus variable:*/
        currentFocus--;
        /*and and make the current item more visible:*/
        addActive(x);
      } else if (e.keyCode == 13) {
        // display_leaflet_map()
        /*If the ENTER key is pressed, prevent the form from being submitted,*/
        e.preventDefault();
        if (currentFocus > -1) {
          /*and simulate a click on the "active" item:*/
          if (x) x[currentFocus].click();
        }
      }
    });
    function addActive(x) {
      /*a function to classify an item as "active":*/
      if (!x) return false;
      /*start by removing the "active" class on all items:*/
      removeActive(x);
      if (currentFocus >= x.length) currentFocus = 0;
      if (currentFocus < 0) currentFocus = (x.length - 1);
      /*add class "cities-active":*/
      x[currentFocus].classList.add("cities-active");
    }
    function removeActive(x) {
      /*a function to remove the "active" class from all autocomplete items:*/
      for (var i = 0; i < x.length; i++) {
        x[i].classList.remove("cities-active");
      }
    }
    function closeAllLists(elmnt) {
      /*close all autocomplete lists in the document,
      except the one passed as an argument:*/
      var x = document.getElementsByClassName("cities-items");
      for (var i = 0; i < x.length; i++) {
        if (elmnt != x[i] && elmnt != ids['city']) {
        x[i].parentNode.removeChild(x[i]);
      }
    }
  }
  /*execute a function when someone clicks in the document:*/
  document.addEventListener("click", function (e) {
      closeAllLists(e.target);
  });
  }

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

//function update_city_data_from_geoname_webservice() {
//
////    update_french_city_name_and_context(latitude, longitude);
//
//    update_city_time_zone();
//
//}

function update_french_city_name_and_context(latitude, longitude) {

      var xmlhttp = new XMLHttpRequest()

      xmlhttp.onreadystatechange = function() {

          if (this.readyState == 4 && (this.status == 200 || this.status == 0)) {

              var data =  JSON.parse(xmlhttp.responseText);

              var feature = data.features[0];
              if (feature) {
                  var city = feature.properties.city
                  var context = feature.properties.context
              } else {
                  var city = ""
                  var context = "Localité hors de France"
              }

//              var id_city = document.getElementById('id_city')
//              var id_context = document.getElementById('id_context')

              id_city.value = city
              id_context.value = context

      	   } else if (this.readyState < 4) {
      			// document.getElementById("loader").style.display = "inline";
      	   }
      };

      var lat = encodeURIComponent(latitude);
      var lon = encodeURIComponent(longitude);

      var q = "lon=" + lon + '&lat='+ lat

      var uri = 'https://api-adresse.data.gouv.fr/reverse/?' + q;

      const encoded = encodeURI(uri);

      xmlhttp.open("GET", encoded);

      xmlhttp.send(null);

}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}


function update_city_data_from_geoname_webservice() {

    var form = '#id-new-theme-form';

//    var data = {'latitude': latitude, 'longitude': longitude}
    var csrftoken = getCookie('csrftoken');

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $.ajax({
        url: "/geo/service/",
        type: "POST",
        data: $(form).serialize(),
        success: function(data) {
//              for (key in data) {
//                  alert(data[key])
//              }
            if (!(data['success'])) {
              $(form).find('.error-message').show()
            }
            else {
               id_latitude.value = data['location'].latitude
               id_longitude.value = data['location'].longitude
               id_city.value = data['location'].city
               id_context.value = data['location'].context
               id_time_zone.value = data['location'].time_zone
            }
        },
        error: function () {
            $(form).find('.error-message').show()
        }
    });


//      var xmlhttp = new XMLHttpRequest()
//
//      xmlhttp.onreadystatechange = function() {
//
//          if (this.readyState == 4 && (this.status == 200 || this.status == 0)) {
//
//              var data =  JSON.parse(xmlhttp.responseText);
//
//              var id_time_zone = document.getElementById('id_time_zone')
//
//              id_time_zone.value = data['time_zone']
//
//      	   } else if (this.readyState < 4) {
//      			// document.getElementById("loader").style.display = "inline";
//      	   }
//      };
//
//      var lat = encodeURIComponent(latitude);
//      var lon = encodeURIComponent(longitude);
//
//      var uri = 'time_zone'
//
//      var csrftoken = getCookie('csrftoken');
//      alert(csrftoken);
//      const encoded = encodeURI(uri);
//
//      xmlhttp.open("POST", encoded, true);
//      xmlhttp.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
//      var data = {'latitude=': lat, 'longitude': lon, 'csrfmiddlewaretoken': window.CSRF_TOKEN }
//      xmlhttp.send({'data': data});

}
