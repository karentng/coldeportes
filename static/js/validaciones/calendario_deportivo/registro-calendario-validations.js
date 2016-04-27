form = "#form-registro-calendario";
fields = {
            cupo_atletas: {
                validators: {
                    notEmpty: {
                        message: 'El evento debe tener un cupo de atletas'
                    },
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
                    notEmpty: {
                        message: 'El evento debe tener un cupo de personas'
                    },
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
                        message: 'El valor ingresado no es una fecha válida, verifique que no sea mayor a la de finalización',
                        format: 'YYYY-MM-DD h:m',
                        max: 'fecha_finalizacion'
                    }
                }
            },
            fecha_finalizacion: {
                validators: {
                    notEmpty: {
                        message: 'La fecha de finalización del evento no puede ser vacía'
                    },
                    date: {
                        message: 'El valor ingresado no es una fecha válida',
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
                        message: 'El valor ingresado no es una fecha válida, debe ser menor a la de finalización de preinscripción',
                        format: 'YYYY-MM-DD h:m',
                        max: 'fecha_finalizacion_preinscripcion'
                    }
                }
            },
            fecha_finalizacion_preinscripcion: {
                validators: {
                    notEmpty: {
                        message: 'La fecha de finalización de la preinscripción del evento no puede ser vacía'
                    },
                    date: {
                        message: 'El valor ingresado no es una fecha válida, debe ser mayor a la de inicio de la preinscripción',
                        format: 'YYYY-MM-DD h:m',
                        min: 'fecha_inicio_preinscripcion'
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
