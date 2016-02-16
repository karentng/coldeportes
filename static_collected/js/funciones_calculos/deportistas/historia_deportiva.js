/**
 * Created by daniel on 30/07/15.
 */
$(document).ready(function() {
    $('#id_fecha_final').prop('required',true);
    /*$("#id_actual").change(function(){
       if($(this).is(":checked")){
           $("#id_fecha_final").val("");
           $("#id_fecha_final").parent().css('display','none');
           $('#id_fecha_final').prop('required',false);
           $(form).bootstrapValidator('removeField','fecha_final');

       }else{
           $("#id_fecha_final").parent().css('display','block');
           $('#id_fecha_final').prop('required',true);
           fields['fecha_final'] = {
               validators: {
                   notEmpty: {
                       message: 'La fecha de inicio de campeonato no puede ser vacía'
                   },
                   date: {
                       message: 'El valor ingresado no es una fecha válida',
                       format: 'YYYY-MM-DD',
                       min: 'fecha_inicial'
                   }
               }
           };
           $(form).bootstrapValidator('addField', 'fecha_final');
           $(form).bootstrapValidator('revalidateField', 'fecha_final');
       }
    });*/
});