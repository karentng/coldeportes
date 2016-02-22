form = "#form-wizard-selecciones";
fields = {
            fecha_inicial: {
                validators: {
                    notEmpty: {
                        message: 'La fecha de convocatoria no puede ser vacía'
                    },
                    date: {
					    message: 'El valor ingresado no es una fecha válida',
                        format: 'YYYY-MM-DD',
                        min: ($.datepicker.formatDate('yy-mm-dd', new Date())).toString(),
                        message: 'La fecha de convocatoria no puede ser menor que hoy o ser mayor a la fecha de fin de convocatoria',
                        max: 'fecha_final',
				    }
                }
            },
            fecha_final: {
                validators: {
                    notEmpty: {
                        message: 'La fecha de finalización de convocatoria no puede ser vacía'
                    },
                    date: {
					    message: 'El valor ingresado no es una fecha válida',
                        format: 'YYYY-MM-DD',
                        message: 'La fecha de finalización de convocatoria no puede ser menor a la fecha de convocatoria',
                        min: 'fecha_inicial'

				    }
                }
            },
            nombre: {
                validators: {
                    notEmpty: {
                        message: 'El nombre de selección no puede ser vacío'
                    }
                }
            },
            campeonato: {
                validators: {
                    notEmpty: {
                        message: 'El nombre de campeonato no puede ser vacío'
                    },
                }
            },
            tipo: {
                validators: {
                    notEmpty: {
                        message: 'Por favor escoja un tipo de selección'
                    },
                }
            },
            tipo_campeonato: {
                validators: {
                    notEmpty: {
                        message: 'Por favor escoja un tipo de campeonato'
                    },
                }
            }

        };
//Revalidar campos al ser actualizados
    $("#id_fecha_inicial").on('change',function(e){
        $(form).bootstrapValidator('revalidateField', 'fecha_inicial');
        $(form).bootstrapValidator('revalidateField', 'fecha_final');
    });
    $("#id_fecha_final").on('change',function(e){
        $(form).bootstrapValidator('revalidateField', 'fecha_inicial');
        $(form).bootstrapValidator('revalidateField', 'fecha_final');
    });
$.getScript(base+"js/validaciones/validations-base.js");
