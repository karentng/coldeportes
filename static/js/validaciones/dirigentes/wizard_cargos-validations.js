form = "#form-wizard-cargos";
fields = {
    nombre: {
        validators: {
            notEmpty: {
                message: 'El cargo del dirigente no puede ser vacío'
            }
        }
    },
    fecha_posesion: {
        validators: {
            notEmpty: {
                message: 'La fecha de posesión del dirigente no puede ser vacía'
            },
            date: {
                message: 'El valor ingresado no es una fecha válida',
                format: 'YYYY-MM-DD',
                max: 'fecha_retiro'
            }
        }
    },
    fecha_retiro: {
        validators: {
            date: {
                message: 'El valor ingresado no es una fecha válida',
                format: 'YYYY-MM-DD',
                min: 'fecha_posesion'
            }
        }
    },
};
//Revalidar campos al ser actualizados
$("#id_fecha_posesion").on('change',function(e){
    $("#form-wizard-cargos").bootstrapValidator('revalidateField', 'fecha_posesion');
});
$("#id_fecha_retiro").on('change',function(e){
    $("#form-wizard-cargos").bootstrapValidator('revalidateField', 'fecha_retiro');
});
$.getScript(base+"js/validaciones/validations-base.js");