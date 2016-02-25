/**
 * Created by daniel on 2/09/15.
 */
var table = $('#tabla-person-seleccionados').DataTable();
var str_no_option = "<p align='center'>Seleccione un personal</p>";

$(document).on("change","#sele-per",function(e){
    var id_per = $(this).val();
    if(id_per){
        var id_entidad = $(this).find(':selected').attr('data_entidad');
        $.ajax({
            url: '/selecciones/vista-previa-per/'+id_entidad+'/'+id_per,
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
    var id_per = $(this).attr("data-per");
    $.ajax({
        url: '/selecciones/guardar-personal/'+sele_id+'/'+id_entidad+'/'+id_per,

        success: function(data) {
            $("#bt-seleccionar").attr('disabled',1);
            $("#sele-per").find(':selected').remove();
            table.row.add(data.respuesta).draw();
        }
    });
});

$(document).on('click','.bt-borrar',function(e){
    var id_per = $(this).attr('data-per');
    var id_entidad = $(this).attr('data-entidad');
    var row = table.row($(this).parents('tr'));

    $.ajax({
        url: '/selecciones/borrar-personal/'+sele_id+'/'+id_entidad+'/'+id_per,
        dataType: 'json',
        success: function(data) {
            row.remove().draw();
            var id = data.id;
            var valor = data.valor;
            var entidad = data.entidad;
            $('#sele-per').append($('<option>', {
                value: id,
                text: valor,
                data_entidad: entidad
            }));
            $('#vista-previa').html(str_no_option);
        }
    });
});