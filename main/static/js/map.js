// Note: This example requires that you consent to location sharing when
// prompted by your browser. If you see the error "The Geolocation service
// failed.", it means you probably did not give permission for the browser to
// locate you.


function updateCollectionPointsTable(pointsArray){
  $('#CollectionPointID').find('tr').each(function(){
    $(this).css('display','none')
  })
  for(var pt in pointsArray){
    let tableRow=$('#CollectionPointID').find('#'+pointsArray[pt].id)
    tableRow.css('display','table-row')
  }
}//end of updateCollectionPointsTable


    var map, infoWindow;


    let positions = [];

    function initAutocomplete() {
// create map
        map = new google.maps.Map(document.getElementById('map'), {
            center: new google.maps.LatLng(40.597509,-73.981832),
            zoom: 6,
            mapTypeId: google.maps.MapTypeId.ROADMAP
        });

        var input = document.getElementById('search_block');
        var searchBox = new google.maps.places.SearchBox(input);
        map.controls[google.maps.ControlPosition.TOP_LEFT].push(input); //note: it will shift position of side list

// Bias the SearchBox results towards current map's viewport.
        map.addListener('bounds_changed', function() {

// find the points in the resultsMap after MAP MOVE
            let result_points =[];
            for (var i=0; i<positions.length; i++){
                if( map.getBounds().contains(positions[i].position) ){
                    result_points.push(locations.find(obj => obj.id === positions[i].id));
                }
            }
            updateCollectionPointsTable(result_points);
        });


// create markers based on the location list and add markers to the map
        var geocoder = new google.maps.Geocoder();
        for (i = 0; i < locations.length; i++) {
            geocodeAddress(geocoder, map,locations[i]);
        }//end of forloop


// search box handling
      // Listen for the event fired when the user selects a prediction and retrieve
      // more details for that place.
      searchBox.addListener('places_changed', function() {

        var places = searchBox.getPlaces();

        if (places.length == 0) {
          return;
        }


        // For each place, get the icon, name and location.
        var bounds = new google.maps.LatLngBounds();
        places.forEach(function(place) {
            if (!place.geometry) {
                console.log("Returned place contains no geometry");
                return;
            }
            if (place.geometry.viewport) {
              // Only geocodes have viewport.
                bounds.union(place.geometry.viewport);
            } else {
                bounds.extend(place.geometry.location);
            }
          });
          map.fitBounds(bounds);
      });//end search



// To add the marker to the map, call setMap();
//marker.setMap(map);

      infoWindow = new google.maps.InfoWindow;
      // console.log(navigator.geolocation);
        // Try HTML5 geolocation.
        if (navigator.geolocation) {
          navigator.geolocation.getCurrentPosition(function(position) {
            var pos = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);

            map.setCenter(pos);
          }, function() {
            handleLocationError(true, infoWindow, map.getCenter());
          });
        } else {
          // Browser doesn't support Geolocation
          handleLocationError(false, infoWindow, map.getCenter());
        }
      }//end of initMap

      function geocodeAddress(geocoder, resultsMap, location) {
         geocoder.geocode({'address': location.address}, function(results, status) {
           if (status === 'OK') {
             resultsMap.setCenter(results[0].geometry.location);
             var marker = new google.maps.Marker({
               map: resultsMap,
               position: results[0].geometry.location
             });
             positions.push({
                 "id":location.id,
                 "position":marker.position
             });
             google.maps.event.addListener(marker, 'mouseover', (function(marker) {
                return function() {
                 infoWindow.setPosition(marker.position);
                 infoWindow.setContent(location.address+'<a href="/packages/'+location.id+'/add" class="w3-text-blue"><i>add package</i></a>');
                 infoWindow.open(resultsMap,marker);

                }
             })(marker));
           } else {
             alert(gettext('Geocode was not successful for the following reason: ') + status);
           }
         });
       }


      function showInfoWindow() {
        var marker = this;
        places.getDetails({placeId: marker.placeResult.place_id},
            function(place, status) {
              if (status !== google.maps.places.PlacesServiceStatus.OK) {
                return;
              }
              infoWindow.open(map, marker);
              buildIWContent(place);
            });
      }

      function handleLocationError(browserHasGeolocation, infoWindow, pos) {
        infoWindow.setPosition(pos);
        infoWindow.setContent(browserHasGeolocation ?
                              gettext('Error: We cannot load your location.') :
                              gettext('Error: Your browser doesn\'t support geolocation.'));
        infoWindow.open(map);
      }//end of handleLocationError
