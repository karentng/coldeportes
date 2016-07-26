/**
 * Created by Milton on 04/08/15.
 */
$(document).ready(function() {
    $('#id_fecha_fin').prop('required',true);
    $("#id_actual").change(function(){
       if($(this).is(":checked")){
           $("#id_fecha_fin").parent().css('display','none');
           $('#id_fecha_fin').prop('required',false);
           $(form).bootstrapValidator('removeField','fecha_fin');
       }else{
           $("#id_fecha_fin").parent().css('display','block');
           $('#id_fecha_fin').prop('required',true);
           fields['fecha_fin'] = {
               validators: {
                   notEmpty: {
                       message: 'La fecha de inicio de campeonato no puede ser vacía'
                   },
                   date: {
                       message: 'El valor ingresado no es una fecha válida',
                       format: 'YYYY-MM-DD',
                       min: 'fecha_comienzo'
                   }
               }
           };
           $(form).bootstrapValidator('addField', 'fecha_fin');
           $(form).bootstrapValidator('revalidateField', 'fecha_fin');
       }
    });
    var modalidad = $("#id_modalidad");
    if (!modalidad.val()){
        modalidad.prop("disabled", true);
    }
    
});

$("#id_deporte").on('change',function(){
    var valor_deporte = $(this).val();
    ajax_modalidades(valor_deporte);
});

function ajax_modalidades(deporte){
    $("#id_modalidad").empty();
    $.ajax({
        url: '/personal-apoyo/modalidades/get/' + deporte,
        dataType: 'json',
        success: function(response) {
            $("#id_modalidad").prop("disabled", false);
            var datos = response.data;
            $("#id_modalidad").select2({
              data: datos
            })
        },
        error: function(err){
            $("#id_modalidad").prop("disabled", true);
            $("#id_modalidad").select2({
              data: null
            });
            $("#id_modalidad").empty();
            console.log(err)
        }
    });
}