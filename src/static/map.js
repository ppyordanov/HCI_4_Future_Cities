var map;
var infowindow = new google.maps.InfoWindow();
	var rectArr=[];
	var cols=["red","blue","green","yellow","orange","gray"]

  function initialize() {
    var rectangle;
    var coachella = new google.maps.LatLng(33.6803003, -116.173894);
    var myOptions = {
      zoom: 12,
      center: coachella,
      mapTypeId: google.maps.MapTypeId.TERRAIN
    };
   map = new google.maps.Map(document.getElementById("map_canvas"),
        myOptions);
	 drawRects();
 	}



function drawRects () {
	 var NW=new google.maps.LatLng(33.7374, -116.39807)
	 var width = 50;
	 var height = 15;

	var NS = google.maps.geometry.spherical.computeOffset(NW,1000,90)
	var SS = google.maps.geometry.spherical.computeOffset(NW,1000,180)
	for (var i = 0; i < height; i++) {
	NE = google.maps.geometry.spherical.computeOffset(NS,i*1000,180)
	SW = google.maps.geometry.spherical.computeOffset(SS,i*1000,180)
	for (var a = 0; a < width; a++) {
	var rectangle = new google.maps.Rectangle();
	var rectOptions = {
        strokeColor: "#FF0000",
        strokeOpacity: 0.8,
        strokeWeight: 2,
        fillColor: cols[Math.floor(Math.random()*cols.length)],
        fillOpacity: 0.35,
        map: map,
        bounds: new google.maps.LatLngBounds(SW,NE)
      };
      rectangle.setOptions(rectOptions);
	  rectArr.push(rectangle);
	  bindWindow(rectangle,rectArr.length)

	var SW = google.maps.geometry.spherical.computeOffset(SW,1000,90)
	var NE = google.maps.geometry.spherical.computeOffset(NE,1000,90)
				}
		}
	}

	  function bindWindow(rectangle,num){
	  google.maps.event.addListener(rectangle, 'click', function(event) {
	  	  infowindow.setContent("you clicked on rectangle "+num)
          infowindow.setPosition(event.latLng)
		  infowindow.open(map);
        });
	  }