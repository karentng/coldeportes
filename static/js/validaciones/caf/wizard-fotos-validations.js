form = "#wizard-fotos-validations";
fields = {
    foto: {
        validators: {
            file: {
                extension: 'png,jpg,jpeg,svg',
                message: 'Seleccione una imagen con alguno de los siguientes formatos (png, jpg, jpeg, svg)'
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