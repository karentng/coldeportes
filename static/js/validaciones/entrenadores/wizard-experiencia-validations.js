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
                message: 'El valor ingresado no es una fecha válida, verifique que no sea mayor a la de finalización',
                format: 'YYYY-MM-DD',
                max: 'fecha_fin'
            }
        }
    },
    fecha_fin: {
        validators: {
            notEmpty: {
                message: 'La fecha de finalización no puede ser vacía'
            },
            date: {
                message: 'El valor ingresado no es una fecha válida, verifique que no sea menor a la de comienzo',
                format: 'YYYY-MM-DD',
                min: 'fecha_comienzo'
            }
        }
    }
};
//Revalidar campos al ser actualizados
    $("#id_fecha_comienzo").on('change',function(e){
        $(form).bootstrapValidator('revalidateField', 'fecha_comienzo');
        $(form).bootstrapValidator('revalidateField', 'fecha_fin');
    });
//Revalidar campos al ser actualizados
    $("#id_fecha_fin").on('change',function(e){
        $(form).bootstrapValidator('revalidateField', 'fecha_comienzo');
        $(form).bootstrapValidator('revalidateField', 'fecha_fin');
    });
$.getScript(base+"js/validaciones/validations-base.js");
