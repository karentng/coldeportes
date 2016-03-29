form = "#form-adjunto-solicitud";
fields = {
            archivo: {
                validators: {
                    file: {
                        extension: 'png,jpg,jpeg,svg,pdf',
                        message: 'Seleccione un archivo con alguno de los siguientes formatos (png, jpg, jpeg, svg, pdf) cuyo tamaño sea menor a 5MB',
                        maxSize: 5242880, // 5MB: http://www.beesky.com/newsite/bit_byte.htm
                    }
                }
            }
        };
$.getScript(base+"js/validaciones/validations-base.js");
