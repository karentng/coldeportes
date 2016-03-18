/**
 * Created by juandgc on 17/02/16.
 */
$(document).ready(function(){
    var $grid = $('#card-container').imagesLoaded( function() {
        // init Masonry after all images have loaded
        $grid.masonry({
            // options...
            itemSelector: '.card',
            columnWidth: 300,
            transitionDuration: '0.8s'
        });
    });

    $(document).on("click",".edicion-clasificados > i",function(){
        var id = $(this).attr("data-id");
        $("#eliminar-clasificado").attr("href","eliminar/"+id);
    });

    $('.add-tooltip').tooltip();
    var $buscador_object = $("#buscador");

    $("#id_categoria").val("Categoria del clasificado");

    $("#id_categoria").on("change",function(e){filter(e)});
    $buscador_object.on("keyup",function(e){filter(e)});

    var filter = function(e) {
        var buscador = $buscador_object.val();
        if (e.type == "keyup"){
            if (e.which != 13) {
                return false;
            }
        }else{
            if(e.type != "change"){
                return false;
            }
        }
        var seleccion = $("#id_categoria").val();

        $.post(filtro_url,{'seleccion' : seleccion, 'palabra':buscador, 'csrfmiddlewaretoken': csrf_token})
            .success(function(result){
                var elements = $grid.masonry('getItemElements');
                var $items = $(result);

                $grid.masonry("remove",elements).masonry('layout');
                $grid.append($items).imagesLoaded( function(){
                    $grid.masonry( 'appended',$items);
                });
            });
    };

    $("#refrescar").click(function(){
        $buscador_object.val("");
        $("#id_categoria").prop("selectedIndex",0).change();
    });

    $(document).on("click",".folded-corner",function(){
        var $this = $(this);

        var foto = $this.attr("data-foto");
        var titulo = $this.attr("data-titulo");
        var descripcion = $this.attr("data-descripcion");
        var fecha = $this.attr("data-fecha");
        var contacto = $this.attr("data-contacto");
        var valor = $this.attr("data-valor");
        var categoria = $this.attr("data-categoria");
        var etiquetas = $this.attr("data-etiquetas");

        $("#titulo-modal").text(titulo).html();
        $("#id-foto").attr("src",media+foto);
        $("#fecha-pub").text(fecha).html();
        $("#categoria").text(categoria).html();
        $("#contacto").text(contacto).html();
        $("#descripcion").text(descripcion).html();
        $("#etiquetas").append(etiquetas);
        if(valor !="None"){
            $(".ver").show();
            $("#valor").html("$"+valor);
        }else {
            $(".ver").hide();
        }
    });
});