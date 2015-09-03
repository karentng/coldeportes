/**
 * Created by daniel on 2/09/15.
 */
var table = $('#tabla-depor-seleccionados').DataTable();
var str_no_option = "<p align='center'>Seleccione un deportista</p>";

$(document).on("change","#sele-depor",function(e){
    var id_depor = $(this).val();
    if(id_depor){
        var id_entidad = $(this).find(':selected').attr('data_entidad');
        $.ajax({
            url: '/selecciones/vista-previa-depor/'+id_entidad+'/'+id_depor,
            success: function(data) {
                $('#vista-previa').html(data);
            }
        });
    }else{
        $('#vista-previa').html(str_no_option);
    }

});

$(document).on('click','#bt-seleccionar',function(){
    var id_entidad = $(this).attr("data-entidad");
    var id_depor = $(this).attr("data-depor");
    $.ajax({
        url: '/selecciones/guardar-deportista/'+sele_id+'/'+id_entidad+'/'+id_depor,

        success: function(data) {
            $("#bt-seleccionar").attr('disabled',1);
            $("#sele-depor").find(':selected').remove();
            table.row.add(data.respuesta).draw();
        }
    });
});

$(document).on('click','.bt-borrar',function(e){
    var id_depor = $(this).attr('data-depor');
    var id_entidad = $(this).attr('data-entidad');
    var row = table.row($(this).parents('tr'));

    $.ajax({
        url: '/selecciones/borrar-deportista/'+sele_id+'/'+id_entidad+'/'+id_depor,
        dataType: 'json',
        success: function(data) {
            row.remove().draw();
            var id = data.id;
            var valor = data.valor;
            var entidad = data.entidad;
            $('#sele-depor').append($('<option>', {
                value: id,
                text: valor,
                data_entidad: entidad
            }));
        }
    });
});
