form = "#form-wizard-deportiva";
fields = {
            nombre: {
                validators: {
                    notEmpty: {
                        message: 'El nombre del campeonato no puede ser vació'
                    }
                }
            },
            pais: {
                validators: {
                    notEmpty: {
                        message: 'Por favor escoja un país'
                    }
                }
            },
            institucion_equipo: {
                validators: {
                    notEmpty: {
                        message: 'El Club Deportivo no puede ser vació'
                    }
                }
            },
            tipo: {
                validators: {
                    notEmpty: {
                        message: 'Por favor escoja un tipo de campeonato'
                    }
                }
            },
            puesto: {
                validators: {
                    notEmpty: {
                        message: 'El puesto no puede ser vació'
                    },
                    numeric: {
                        message: 'El puesto debe ser numérico'
                    },
                    greaterThan: {
                        message: 'El puesto no puede ser menor o igual a 0',
                        value: 1

                    }
                }
            },
            categoria: {
                validators: {
                    notEmpty: {
                        message: 'La categoría no puede ser vaciá'
                    },
                }
            },
            fecha_inicial: {
                validators: {
                    notEmpty: {
                        message: 'La fecha de inicio de campeonato no puede ser vacía'
                    },
                    date: {
                        message: 'El valor ingresado no es una fecha válida, verifique que no sea mayor a la de finalización',
                        format: 'YYYY-MM-DD',
                        max: 'fecha_final'
                    }
                }
            },
            fecha_final: {
                validators: {
                    date: {
                        message: 'El valor ingresado no es una fecha válida',
                        format: 'YYYY-MM-DD',
                        min: 'fecha_inicial'
                    }
                }
            }

        };
//Revalidar campos al ser actualizados
    $("#id_fecha_inicial").on('change',function(e){
        $(form).bootstrapValidator('revalidateField', 'fecha_inicial');
        $(form).bootstrapValidator('revalidateField', 'fecha_final');
    });
//Revalidar campos al ser actualizados
    $("#id_fecha_final").on('change',function(e){
        $(form).bootstrapValidator('revalidateField', 'fecha_inicial');
        $(form).bootstrapValidator('revalidateField', 'fecha_final');
    });

$.getScript(base+"js/validaciones/validations-base.js");
