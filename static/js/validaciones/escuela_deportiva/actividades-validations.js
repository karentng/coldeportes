form = "#form-actividad";
fields = {
    dirigido_a: {
        validators: {
            notEmpty: {
                message: "El campo Dirigido a no puede ser vacío"
            }
        }
    },
    sede: {
        validators: {
            notEmpty: {
                message: 'El campo Sede no puede ser vacío'
            }
        }
    },
    titulo: {
        validators: {
            notEmpty: {
                message: "El campo Título de actividad no puede ser vacío"
            }
        }
    },
    dia_actividad: {
        validators: {
            notEmpty: {
                message: 'El campo Día actividad no puede ser vacío'
            },
            date: {
                message: 'El valor ingresado no es una fecha válida, debe ser mayor al dia de hoy',
                format: 'YYYY-MM-DD',
                min: function(field, validator){
                    var d = new Date();

                    var curr_date = d.getDate();

                    var curr_month = d.getMonth() + 1;

                    var curr_year = d.getFullYear();
                    return curr_year + "-" + curr_month + "-" + curr_date;

                }
            }
        }
    },
    hora_inicio: {
        validators: {
            notEmpty: {
                message: 'El campo Hora inicio no puede ser vacío'
            }
        }
    },
    hora_fin: {
        validators: {
            notEmpty: {
                message: 'El campo Hora fin no puede ser vacío'
            }
        }
    },
    descripcion: {
        validators: {
            notEmpty: {
                message: 'El campo Descripción fin no puede ser vacío'
            }
        }
    }
};

var $form = $("#form-actividad");

//Revalidar campos al ser actualizados
$("#id_dia_actividad").on('change',function(){
    $form.bootstrapValidator('revalidateField', 'dia_actividad');
});
$("#id_hora_inicio").on('change',function(){
    $form.bootstrapValidator('revalidateField', 'hora_inicio');
});
$("#id_hora_fin").on('change',function(){
    $form.bootstrapValidator('revalidateField', 'hora_fin');
});

$.getScript(base+"js/validaciones/validations-base.js");
