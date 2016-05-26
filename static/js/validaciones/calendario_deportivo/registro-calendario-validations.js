form = "#form-registro-calendario";
fields = {
            cupo_atletas: {
                validators: {
                    numeric: {
                        message: 'El cupo debe ser numérico'
                    },
                    greaterThan: {
                        message: 'El cupo de atletas no puede ser menor o igual a 0',
                        value: 1

                    }
                }
            },
            cupo_personas: {
                validators: {
                    numeric: {
                        message: 'El cupo debe ser numérico'
                    },
                    greaterThan: {
                        message: 'El cupo de personas no puede ser menor o igual a 0',
                        value: 1

                    }
                }
            },
            fecha_inicio: {
                validators: {
                    notEmpty: {
                        message: 'La fecha de inicio del evento no puede ser vacía'
                    },
                    date: {
                        message: 'Verifique que la fecha de inicio sea mayor al día de hoy y  menor a la de finalización',
                        format: 'YYYY-MM-DD h:m',
                        max: 'fecha_finalizacion',
                        min: hoy()
                    }
                }
            },
            fecha_finalizacion: {
                validators: {
                    notEmpty: {
                        message: 'La fecha de finalización del evento no puede ser vacía'
                    },
                    date: {
                        message: 'La fecha de finalización debe ser mayor a la fecha de inicio',
                        format: 'YYYY-MM-DD h:m',
                        min: 'fecha_inicio'
                    }
                }
            },
            fecha_inicio_preinscripcion: {
                validators: {
                    notEmpty: {
                        message: 'La fecha de inicio de la preinscripción del evento no puede ser vacía'
                    },
                    date: {
                        message: 'Verifique que la fecha de preinscripcion sea mayor al dia de hoy y menor la fecha de inicio del evento',
                        format: 'YYYY-MM-DD h:m',
                        max: 'fecha_inicio',
                        min: hoy()
                    }
                }
            },
            fecha_finalizacion_preinscripcion: {
                validators: {
                    notEmpty: {
                        message: 'La fecha de finalización de la preinscripción del evento no puede ser vacía'
                    },
                    date: {
                        message: 'Verifique que la fecha de cierre de preinscripcion sea mayor a la fecha de inicio de preinscripcion y menor a la fecha de inicio del evento',
                        format: 'YYYY-MM-DD h:m',
                        min: 'fecha_inicio_preinscripcion',
                        max: 'fecha_inicio'
                    }
                }
            },
            objetivo: {
                validators: {
                    notEmpty: {
                        message: 'El evento debe tener un objetivo'
                    },
                    stringLength: {
                        message: 'El tamaño del objetivo debe tener como maximo 200 caracteres',
                        max: 200
                    }

                }
            }

        };

function hoy(){
    var dia = ($.datepicker.formatDate('yy-mm-dd', new Date())).toString();
    var hora = new Date();
    return dia+" "+hora.getHours()+":"+hora.getMinutes();
}
//Revalidar campos al ser actualizados
    $("#id_fecha_inicio").on('change',function(e){
        $(form).bootstrapValidator('revalidateField', 'fecha_inicio');
    });
//Revalidar campos al ser actualizados
    $("#id_fecha_finalizacion").on('change',function(e){
        $(form).bootstrapValidator('revalidateField', 'fecha_inicio');
        $(form).bootstrapValidator('revalidateField', 'fecha_finalizacion');
    });

//Revalidar campos al ser actualizados
    $("#id_fecha_inicio_preinscripcion").on('change',function(e){
        $(form).bootstrapValidator('revalidateField', 'fecha_inicio_preinscripcion');
    });
//Revalidar campos al ser actualizados
    $("#id_fecha_finalizacion_preinscripcion").on('change',function(e){
        $(form).bootstrapValidator('revalidateField', 'fecha_inicio_preinscripcion');
        $(form).bootstrapValidator('revalidateField', 'fecha_finalizacion_preinscripcion');
    });
$.getScript(base+"js/validaciones/validations-base.js");
