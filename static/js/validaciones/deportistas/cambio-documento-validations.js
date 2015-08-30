form = "#form-cambio-documento";
fields = {
            tipo_documento_anterior: {
                validators: {
                    notEmpty: {
                        message: 'Este campo no puede estar vacío'
                    }
                }
            },
            identificacion_anterior: {
                validators: {
                    notEmpty: {
                        message: 'Este campo no puede estar vacío'
                    }
                }
            },
            tipo_documento_nuevo: {
                validators: {
                    notEmpty: {
                        message: 'Por favor seleccione un tipo de documento'
                    }
                }
            },
            identificacion_nuevo: {
                validators: {
                    notEmpty: {
                        message: 'El nuevo valor de identificación no puede ser vacío'
                    }
                }
            }

        };
$.getScript(base+"js/validaciones/validations-base.js");
