/**
 * Created by Milton on 04/08/15.
 */
$(document).ready(function() {
    $('#id_fecha_fin').prop('required',true);
    $("#id_actual").change(function(){
       if($(this).is(":checked")){
           $("#id_fecha_fin").val("");
           $("#id_fecha_fin").parent().css('display','none');
           $('#id_fecha_fin').prop('required',false);
           delete fields['fecha_final'];

       }else{
           $("#id_fecha_fin").parent().css('display','block');
           $('#id_fecha_fin').prop('required',true);
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
           $(form).bootstrapValidator('revalidateField', 'fecha_final');
       }
    });
    App.init();
    FormWizard.init();
});