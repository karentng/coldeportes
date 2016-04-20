form = "#form-actividad";

$.getScript(base+"plugins/moment/moment.min.js");
fields = {
    titulo: {
        validators: {
            notEmpty: {
                message: "El título de la actividad no puede ser vacío"
            }
        }
    },
    descripcion: {
        validators: {
            notEmpty: {
                message: "la descripcion de la actividad no puede ser vacío"
            }
        }
    },
    dia_actividad: {
        validators: {
            notEmpty: {
                message: 'El día de la activiadad no puede ser vacía'
            },
            date: {
                message: 'El valor ingresado no es una fecha válida',
                format: 'YYYY-MM-DD'
            },
            callback:{
                message: "El valor ingresado no es una fecha válida, debe estar entre las fechas del evento",
                callback: function(field, validator){
                    var momento = new moment(field, 'YYYY-MM-DD', true);
                    if (!momento.isValid()) {
                        return false;
                    }
                    return momento.isSameOrAfter(fecha_in) && momento.isSameOrBefore(fecha_fn);

                }
            }
        }
    },
    hora_inicio: {
        validators: {
            notEmpty: {
                message: 'La hora de inicio de la actividad no puede ser vacía'
            }
        }
    },
    hora_fin: {
        validators: {
            notEmpty: {
                message: 'La hora de finalización de la actividad no puede ser vacía'
            }
        }
    }
};



//Revalidar campos al ser actualizados
$("#id_dia_actividad").on('change',function(e){
    $(form).bootstrapValidator('revalidateField', 'dia_actividad');
});
$("#id_hora_inicio").on('change',function(e){
    $(form).bootstrapValidator('revalidateField', 'hora_inicio');
});
$("#id_hora_fin").on('change',function(e){
    $(form).bootstrapValidator('revalidateField', 'hora_fin');
});

$.getScript(base+"js/validaciones/validations-base.js");
