form = "#noticia";
fields = {
    foto: {
        validators: {
            file: {
                extension: 'png,jpg,jpeg,svg',
                message: 'Seleccione una imagen con alguno de los siguientes formatos (png, jpg, jpeg, svg) y que tenga un tamaño menor a 5MB',
                maxSize: 5242880 //5MB
            }
        },
    },
    titulo: {
        validators: {
            notEmpty: {
                message: "El título de la noticia no puede ser vacío"
            }
        }
    },
    cuerpo_noticia: {
        validators: {
            notEmpty: {
                message: "El cuerpo de la noticia no puede ser vacío"
            }
        }
    }
};
$.getScript(base+"js/validaciones/validations-base.js");