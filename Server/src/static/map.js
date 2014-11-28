var minLatBounds = 55.710672;
var maxLatBounds = 56.019295;
var minLonBounds = -3.930433;
var maxLonBounds = -4.701437;
var centerLocation = new google.maps.LatLng(55.8554602, -4.2324586);
var NOIMAGE = "/static/images/noimage.png";
var GOOD = "good";
var BAD = "bad";
var NO_INFO = "No data";

var MAP_CANVAS = "#map_canvas";
var $selector = MAP_CANVAS;

var map;
var infowindow = new google.maps.InfoWindow();
var rectArr = [];
//var COLOR_DATA=["red","blue","green","yellow","orange","gray"];
var COLOR_DATA = [["gray", 0.2], ["yellow",0.2], ["#81B33A",0.5]]; //COLOR > OPACITY

var user_data;
var photo_list;

$(document).ready(function(){

    initialize();

});

$(document).on('click', $selector, function(e){

        $("[rel='tooltip']").tooltip();
        $('.thumbnail').hover(
        function(){
            $(this).find('.caption').slideDown(250); //.fadeIn(250)
        },
        function(){
            $(this).find('.caption').slideUp(250); //.fadeOut(205)
        });




});

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
            var NUM = (i*width + a)+1;
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

function metaData(title, description, user, weather){
    return "<div class='META topmin'>" + "<b>Weather:</b> " + weather + "<br>" + "<b>Title:</b> " +  title + "<br>" + "<b>Description:</b> "  + description + "<br>" + "<b>Uploaded by:</b> "  + user +  "</div>";
}

function modalBox(photo, id){

    var content = "<div class='fade modal' id='" + id +"'><div class='modal-dialog modal-content'>";
    content += "<div class='modal-content span7 text-center'>";
    content += "<img class='topplusmore myImg' src=" + photo + "></img><br>";
    content += "<a hreg='#' rel='tooltip' title='Rate up' class='btn btn-success glyphicon glyphicon-thumbs-up'></a>";
    content += " <a hreg='#'  rel='tooltip' title='Rate down' class='btn btn-danger glyphicon glyphicon-thumbs-down'></a>";
    content += " <a href='" + photo + "'  rel='tooltip' download='" + photo +"' title='Download' class='btn btn-primary glyphicon glyphicon-download-alt'></a>";
    content += " <a data-dismiss='modal' class='btn btn-default '>Close</a>";
    content += "</div></div></div>";

    /*
    content+=       "<div id='" + id +"' class='fade modal' style='display: none; '>" +
                    "<div class='modal-dialog modal-content'><h3>Preview Photo</h3>" +
					"<div class='modal-body'><img class='topplusmore myImg' src=" + photo + "/>" +
					"</div><div class='modal-footer'>" +
					"<a href='#' rel='tooltip' title='Rate up' class='btn btn-success glyphicon glyphicon-thumbs-up'></a>" +
					"<a href='#' rel='tooltip' title='Rate up' class='btn btn-success glyphicon glyphicon-thumbs-up'></a>" +
					"<a href='" + photo + "'  rel='tooltip' download='" + photo +"' title='Download' class='btn btn-primary glyphicon glyphicon-download-alt'></a>" +
                    "<a href='#' rel='tooltip' title='OK' class='btn btn-success glyphicon glyphicon-ok-sign' data-dismiss='modal'></a>" +
                    "</div></div></div>";
    */

    return content

}

function tooltip(photo, id){
    var content ="";
    content = "<div class='span7 text-center'><a data-toggle='modal' href='#" + id +"' rel='tooltip' title='Preview photo.' class=' glyphicon glyphicon-eye-open btn btn-default'></a> ";
    content += modalBox(photo, id);
    content += "<a href='/update' rel='tooltip' id='update' title='Update photo.' class='glyphicon glyphicon-collapse-up btn btn-default'></a>";
    content += "</div>";


    return content;
}

function thumbNail(photo, id){


    var content = "";
    content +="<div id='pre' class='META thumbnail topplus'>";
    content+="<div class='caption'>" + tooltip(photo, id) +"</div>";
    content += "<img class='myImg' height='200' width='200' src=" + photo + "></img>";
    content +="</div>";
    return content;
}

function generatePopUpContent(num){
    var status = getStatus(num);
    var good_weather = NOIMAGE;
    var bad_weather = NOIMAGE;

    var good_photo;
    var bad_photo;

    var gtitle = NO_INFO;
    var btitle = NO_INFO;
    var gweather = NO_INFO;
    var bweather = NO_INFO;
    var gdesc = NO_INFO;
    var bdesc = NO_INFO;
    var guser = NO_INFO;
    var buser = NO_INFO;

    if(status == 1){
        if(GOOD in photo_list[num]){
            good_photo = photo_list[num][GOOD];
            good_weather = good_photo.photo;
            gtitle = good_photo.title;
            gdesc = good_photo.description;
            guser = good_photo.userid;
            gweather = good_photo.weather;
        }
        else{
            bad_photo = photo_list[num][BAD];
            bad_weather = bad_photo.photo;
            btitle = bad_photo.title;
            bdesc = bad_photo.description;
            buser = bad_photo.userid;
            bweather = bad_photo.weather;
        }
    }
    else if(status == 2){
        good_photo = photo_list[num][GOOD];
        bad_photo = photo_list[num][BAD];
        good_weather = good_photo.photo;
        bad_weather = bad_photo.photo;

        gtitle = good_photo.title;
        gdesc = good_photo.description;
        guser = good_photo.userid;
        gweather=good_photo.weather;
        btitle = bad_photo.title;
        bdesc = bad_photo.description;
        buser = bad_photo.userid;
        bweather =bad_photo.weather;
    }

    var content = "<b>Square " + num + "</b><br>";
    content += thumbNail(good_weather, 1);
    content += thumbNail(bad_weather, 2);
    content += "<br>";
    content += metaData(gtitle, gdesc, guser, gweather);
    content += metaData(btitle, bdesc, buser, bweather);

    return content;
}

function bindWindow(rectangle, num) {
    google.maps.event.addListener(rectangle, 'click', function (event) {

        infowindow.setContent(generatePopUpContent(num));


        /*
        if(num in photo_list){
            infowindow.setContent(generatePopUpContent(num));
        }
        else{
            infowindow.setContent("Square " + num + ". Upload a photo from this location to get points!");
        }
        */

        infowindow.setPosition(event.latLng);
        infowindow.open(map);
    });
}
