form = "#form-actividad";
$.getScript(base+"plugins/moment/moment.min.js");
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
                message: 'La hora del inicio no puede ser vacío'
            }
        }
    },
    hora_fin: {
        validators: {
            notEmpty: {
                message: 'La hora final no puede ser vacía'
            },
            callback:{
                message: "El valor ingresado no es una hora válida, debe ser mayor a la hora de inicio",
                callback: function(field, validator){
                    var inicio = $("input#id_hora_inicio").val();

                    var momento = new moment(field, 'HH:mm', true);
                    var momentInit = new moment(inicio, 'HH:mm', true);
                        console.log(field);
                    if (!momento.isValid()) {
                        console.log(momento);
                        return false;
                    }
                    return momento.isAfter(momentInit);

                }
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

$("#id_hora_inicio").on('change',function(e){
    $form.bootstrapValidator('revalidateField', 'hora_inicio');
    $form.bootstrapValidator('revalidateField', 'hora_fin');
});
$("#id_hora_fin").on('change',function(e){
    $form.bootstrapValidator('revalidateField', 'hora_inicio');
    $form.bootstrapValidator('revalidateField', 'hora_fin');
});

$.getScript(base+"js/validaciones/validations-base.js");
