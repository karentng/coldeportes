form = "#form-wizard-lesiones";
fields = {
            tipo_lesion: {
                validators: {
                    notEmpty: {
                        message: 'Por favor escoja un tipo de lesión'
                    }
                }
            },
            fecha_lesion: {
                validators: {
                    notEmpty: {
                        message: 'Por favor ingrese una fecha en la que sufrió la lesión'
                    },
                    date: {
					    message: 'El valor ingresado no es una fecha válida',
                        format: 'YYYY-MM-DD',
                        message: 'La fecha de la lesión no puede ser mayor a hoy',
                        max: ($.datepicker.formatDate('yy-mm-dd', new Date())).toString()
				    }
                }
            },
            periodo_rehabilitacion: {
                validators: {
                    notEmpty: {
                        message: 'Por favor escoja un periodo de rehabilitación'
                    }
                }
            },

        };

//Revalidar campos al ser actualizados
    $("#id_fecha_lesion").on('change',function(e){
        $(form).bootstrapValidator('revalidateField', 'fecha_lesion');
    });
$.getScript(base+"js/validaciones/validations-base.js");
