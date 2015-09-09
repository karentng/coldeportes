var datosMostrar = arrayToJson(datosMostrar);
var posicionInicial = arrayToJson(posicionInicial);

function informacion(ventana ,marker, map){
    marker.addListener('click', function() {
        ventana.open(map, marker);
    });
}

var map;
function initMap() {
    var myLatLng = {lat: posicionInicial[0], lng: posicionInicial[1]};
    map = new google.maps.Map(document.getElementById(mapa), {
        center: myLatLng,
        zoom: 12
    });

    for(i in datosMostrar){
        var datos = datosMostrar[i];

        var imagen = datos[0];
        var titulo = datos[4];
        var latitud = datos[2];
        var longitud = datos[3];
        var datos = datos[1];
        
        var contenido = "";
        for(j in datos){
            contenido += '\
            <div class="row">\
                <div class="col-sm-4 col-md-3">\
                    <b>'+datos[j][0]+':</b>\
                </div>\
                <div class="col-sm-8 col-md-9">\
                    '+datos[j][1]+'\
                </div>\
            </div>';
        }
        
        var ventana = new google.maps.InfoWindow({
            content:
                    '<div class="col-md-4">\
                        <img src="'+imagen+'" alt="imagen" style="width:100%;height:100%">\
                    </div>\
                    <div class="col-md-8">\
                        '+contenido+'\
                    </div>'
        });
        var posicion = {lat: latitud, lng: longitud};
        var marker = new google.maps.Marker({
            position: posicion,
            map: map,
            title: titulo,
        });
        informacion(ventana, marker, map);
    }
}