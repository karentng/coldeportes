form = "#wizard-fotos-validations";
fields = {
    foto: {
        validators: {
            file: {
                extension: 'png,jpg,jpeg,svg',
                message: 'Seleccione una imagen con alguno de los siguientes formatos (png, jpg, jpeg, svg) cuyo tamaño sea menor a 5MB',
                maxSize: 5242880, // 5MB: http://www.beesky.com/newsite/bit_byte.htm
            },
            notEmpty: {
                message: 'Debe seleccionar una imagen'
            }
        }
    },
    titulo: {
        validators: {
            notEmpty: {
                message: 'El título no puede ser vacío'
            }
        }
    },
};
$.getScript(base+"js/validaciones/validations-base.js");