form = '#form-formacion';
fields = {
    disciplina_deportiva: {
        validators: {
            notEmpty: {
                message: 'Escoja al menos una disciplina deportiva'
            }
        }
    },
    denominacion_diploma: {
        validators: {
            notEmpty: {
                message: 'La denominación del diploma no puede ser vacía'
            }
        }
    },
    nivel: {
        validators: {
            notEmpty: {
                message: 'El nivel no puede ser vacío'
            }
        }
    },
    institucion_formacion: {
        validators: {
            notEmpty: {
                message: 'La institución de formación no puede ser vacía'
            }
        }
    },
    pais_formacion: {
            validators: {
                notEmpty: {
                message: 'Por favor escoja un país'
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
            date: {
                message: 'El valor ingresado no es una fecha válida, verifique que no sea menor a la de inicio',
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