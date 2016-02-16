form = "#form-wizard-doping";
fields = {
            nombre_delegado: {
                validators: {
                    notEmpty: {
                        message: 'El nombre del delegado no puede ser vacío'
                    }
                }
            },
            tipo_identidad_delegado: {
                validators: {
                    notEmpty: {
                        message: 'Por favor escoja un tipo de identificación'
                    }
                }
            },
            identificacion_delegado: {
                validators: {
                    notEmpty: {
                        message: 'El número de identificación no puede ser vacío'
                    }
                }
            },
            evento: {
                validators: {
                    notEmpty: {
                        message: 'El evento en el que se detectó el doping no puede ser vacío'
                    }
                }
            },
            fecha: {
                validators: {
                    notEmpty: {
                        message: 'La fecha en la que se detectó el doping no puede ser vacía'
                    },
                    date: {
					    message: 'El valor ingresado no es una fecha válida',
                        format: 'YYYY-MM-DD',
                        message: 'La fecha en la que se detectó el doping no puede ser mayor a hoy',
                        max: ($.datepicker.formatDate('yy-mm-dd', new Date())).toString()
				    }
                }
            }

        };

//Revalidar campos al ser actualizados
    $("#id_fecha").on('change',function(e){
        $(form).bootstrapValidator('revalidateField', 'fecha');
    });
$.getScript(base+"js/validaciones/validations-base.js");
