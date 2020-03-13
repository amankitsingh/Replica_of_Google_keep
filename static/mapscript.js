var map;
var markers = [];
var polygon = null;
var placeMarkers = [];

function initAutocomplete() {
  var styles = [{
    featureType: 'water',
    stylers: [{
      color: '#1AA0C8'
    }]
  }, {
    featureType: 'administrative',
    elementType: 'labels.text.stroke',
    stylers: [{
        color: '#FFFFFF'
      },
      {
        weight: 6
      }
    ]
  }, {
    featureType: 'administrative',
    elementType: 'labels.text.fill',
    stylers: [{
      color: '#EF5113'
    }]
  }, {
    featureType: 'road.highway',
    elementType: 'geometry.stroke',
    stylers: [{
        color: '#EFE9E4'
      },
      {
        lightness: -40
      }
    ]
  }, {
    featureType: 'transit.station',
    stylers: [{
        weight: 9
      },
      {
        hue: '#e85113'
      }
    ]
  }, {
    featureType: 'road.highway',
    elementType: 'labels.icon',
    stylers: [{
      visibility: 'off'
    }]
  }, {
    featureType: 'water',
    elementType: 'labels.text.stroke',
    stylers: [{
      lightness: 100
    }]
  }, {
    featureType: 'water',
    elementType: 'labels.text.fill',
    stylers: [{
      lightness: -100
    }]
  }, {
    featureType: 'poi',
    elementType: 'geometry',
    stylers: [{
        visibility: 'on'
      },
      {
        color: '#F0E4FF'
      }
    ]
  }, {
    featureType: 'road.highway',
    elementType: 'geometry.fill',
    stylers: [{
        color: '#EFE9E4'
      },
      {
        lightness: -25
      }
    ]
  }];

  // Constructor creates a new map .
  map = new google.maps.Map(document.getElementById('map'), {
    center: {
      lat: 12.972249,
      lng: 77.612693
    },
    zoom: 8,
    styles: styles,
    mapTypeControl: false
  });

  // Create the search box and link it to the UI element.
  var input = document.getElementById('pac-input');
  var searchBox = new google.maps.places.SearchBox(input);

  // Bias the SearchBox results towards current map's viewport.
  map.addListener('bounds_changed', function () {
    searchBox.setBounds(map.getBounds());
  });

  var markers = [];
  // Listen for the event fired when the user selects a prediction and retrieve
  // more details for that place.
  searchBox.addListener('places_changed', function () {
    var places = searchBox.getPlaces();

    if (places.length == 0) {
      return;
    }

    // Clear out the old markers.
    markers.forEach(function (marker) {
      marker.setMap(null);
    });
    markers = [];

    // For each place, get the icon, name and location.
    var bounds = new google.maps.LatLngBounds();
    places.forEach(function (place) {
      if (!place.geometry) {
        console.log("Returned place contains no geometry");
        return;
      }
      var icon = {
        url: place.icon,
        size: new google.maps.Size(10, 10),
        origin: new google.maps.Point(0, 0),
        anchor: new google.maps.Point(10, 10),
        scaledSize: new google.maps.Size(10, 10)
      };

      // Create a marker for each place.
      markers.push(new google.maps.Marker({
        map: map,
        icon: icon,
        title: place.name,
        position: place.geometry.location
      }));

      if (place.geometry.viewport) {
        // Only geocodes have viewport.
        bounds.union(place.geometry.viewport);
      } else {
        bounds.extend(place.geometry.location);
      }
    });
    map.fitBounds(bounds);
  });
}