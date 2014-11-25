var minLatBounds = 55.710672;
var maxLatBounds = 56.019295;
var minLonBounds = -3.930433;
var maxLonBounds = -4.701437;
var centerLocation = new google.maps.LatLng(55.8554602, -4.2324586);

var map;
var infowindow = new google.maps.InfoWindow();
var rectArr = [];
//var COLOR_DATA=["red","blue","green","yellow","orange","gray"];
var COLOR_DATA = [["gray", 0.2], ["yellow",0.2], ["#81B33A",0.5]]; //COLOR > OPACITY

var user_data;
var photo_list;

function initialize() {

    loading_animation();

    var myOptions = {
        zoom: 12,
        minZoom: 11,
        center: centerLocation,
        mapTypeId: google.maps.MapTypeId.TERRAIN,
        disableDefaultUI: true

    };
    map = new google.maps.Map(document.getElementById("map_canvas"),
        myOptions);
    drawRects();


    var frameBorder = new google.maps.LatLngBounds(
        new google.maps.LatLng(minLatBounds, maxLonBounds),
        new google.maps.LatLng(maxLatBounds, minLonBounds)
    );

    var lastCenter = map.getCenter();

    google.maps.event.addListener(map, 'center_changed', function () {
        if (frameBorder.contains(map.getCenter())) {

            // save last position within specivied bounds
            lastCenter = map.getCenter();
            return;
        }

        map.panTo(lastCenter);
    });
}

function getStatus(num){
    var result = 0; //GRAY
    if(num in photo_list){
        if(photo_list[num]['good'] != undefined && photo_list[num]['bad']!=undefined){
            result = 2; //GREEN
        }
        else{
        result = 1; //YELLOW
        }

    }

    return result;

}


function drawRects() {
    var NW = new google.maps.LatLng(55.938764, -4.534239);
    var width = 40;
    var height = 20;

    var NS = google.maps.geometry.spherical.computeOffset(NW, 1000, 90);
    var SS = google.maps.geometry.spherical.computeOffset(NW, 1000, 180);
    for (var i = 0; i < height; i++) {
        NE = google.maps.geometry.spherical.computeOffset(NS, i * 1000, 180);
        SW = google.maps.geometry.spherical.computeOffset(SS, i * 1000, 180);
        for (var a = 0; a < width; a++) {
            var NUM = i*width + a;
            var color = getStatus(NUM);
            var rectangle = new google.maps.Rectangle();
            var rectOptions = {
                strokeColor: "#81B33A",
                strokeOpacity: 0.2,
                strokeWeight: 2,
                fillColor: COLOR_DATA[color][0],
                fillOpacity: COLOR_DATA[color][1],
                map: map,
                bounds: new google.maps.LatLngBounds(SW, NE)

            };
            rectangle.setOptions(rectOptions);
            rectArr.push(rectangle);
            bindWindow(rectangle, rectArr.length);

            var SW = google.maps.geometry.spherical.computeOffset(SW, 1000, 90);
            var NE = google.maps.geometry.spherical.computeOffset(NE, 1000, 90)
        }
    }
}


function generatePopUpContent(num){
    var content = "<b>Square " + num + "<b><br>";
    content += photo_list[num]['bad'].title;
    return content;
}

function bindWindow(rectangle, num) {
    google.maps.event.addListener(rectangle, 'mouseover', function (event) {

        if(num in photo_list){
            infowindow.setContent(generatePopUpContent(num));
        }
        else{
            infowindow.setContent("Square " + num + ". Upload a photo from this location to get points!");
        }

        infowindow.setPosition(event.latLng);
        infowindow.open(map);
    });
}
