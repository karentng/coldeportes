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
});