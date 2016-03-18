/**
 * Created by juandgc on 16/03/16.
 */
var geocoder;
var map;
var address = "Cali, Valle del Cauca, Colombia";

function initialize() {
  geocoder = new google.maps.Geocoder();
  var latlng = new google.maps.LatLng(lat, lng);
  var myOptions = {
    zoom: 12,
    center: latlng,
    mapTypeControl: true,
    mapTypeControlOptions: {
      style: google.maps.MapTypeControlStyle.DROPDOWN_MENU
    },
    navigationControl: true,
    mapTypeId: google.maps.MapTypeId.ROADMAP
  };
  map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);

  var marker = new google.maps.Marker({
    position: latlng,
    map: map,
    title: "Palmaseca"
  });
  panorama = map.getStreetView();
  panorama.setPosition(latlng);
  panorama.setVisible(true);
  google.maps.event.addListener(marker, 'click', function() {
    infowindow.open(map, marker);
  });
}
google.maps.event.addDomListener(window, 'load', initialize);