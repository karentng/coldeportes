form = '#form-experiencia';
fields = {
    nombre_cargo: {
        validators: {
            notEmpty: {
                message: 'El nombre del cargo no puede ser vacío'
            }
        }
    },
    institucion: {
        validators: {
            notEmpty: {
                message: 'La institución no puede ser vacía'
            }
        }
    },
    fecha_comienzo: {
        validators: {
            notEmpty: {
                message: 'La fecha de inicio no puede ser vacía'
            },
            date: {
                message: 'El valor ingresado no es una fecha válida',
                format: 'YYYY-MM-DD',
                max: 'fecha_fin'
            }
        }
    },
    fecha_fin: {
        validators: {
            date: {
                message: 'El valor ingresado no es una fecha válida',
                format: 'YYYY-MM-DD',
                max: 'fecha_comienzo'
            }
        }
    }
};
//Revalidar campos al ser actualizados
    $("#id_fecha_comienzo").on('change',function(e){
        $(form).bootstrapValidator('revalidateField', 'fecha_comienzo');
    });
//Revalidar campos al ser actualizados
    $("#id_fecha_fin").on('change',function(e){
        $(form).bootstrapValidator('revalidateField', 'fecha_fin');
    });
$.getScript(base+"js/validaciones/validations-base.js");
