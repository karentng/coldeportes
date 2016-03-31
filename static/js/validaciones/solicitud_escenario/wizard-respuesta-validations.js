form = "#form-respuesta-solicitud";
fields = {
            adjuntos: {
                validators: {
                    file: {
                        extension: 'png,jpg,jpeg,pdf,zip,rar',
                        message: 'Selecciones archivo con alguno de los siguientes formatos (png, jpg, jpeg, pdf, zip, rar) cuyo tamaño sea menor a 5MB',
                        maxSize: 5242880, // 5MB: http://www.beesky.com/newsite/bit_byte.htm
                    }
                }
            },
            descripcion: {
                validators: {
                    notEmpty: {
                        message: 'La descripción no puede ser vacia'
                    }
                }
            },
            estado_actual: {
                validators: {
                    notEmpty: {
                        message: 'Debe escoger un estado'
                    }
                }
            }
        };
$.getScript(base+"js/validaciones/validations-base.js");
