form = "#clasificado-form";
fields = {
    titulo: {
        validators: {
            notEmpty: {
                message: "El título del clasificado no puede ser vacío"
            }
        }
    },
    descripcion: {
        validators: {
            notEmpty: {
                message: "La descripción del clasificado no puede ser vacío"
            }
        }
    },
    contacto: {
        validators: {
            notEmpty: {
                message: "El contacto del clasificado no puede ser vacío"
            }
        }
    }
};
$.getScript(base+"js/validaciones/validations-base.js");