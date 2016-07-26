form = "#form-alerta";
fields = {
    nivel_alerta: {
        validators: {
            notEmpty: {
                message: "El campo Nivel de alerta no puede ser vacío"
            }
        }
    },
    referencia_alerta: {
        validators: {
            notEmpty: {
                message: "El campo Referencia de alerta no puede ser vacío"
            }
        }
    },
    descripcion: {
        validators: {
            notEmpty: {
                message: "El campo Descripción no puede ser vacío"
            }
        }
    }
};

$.getScript(base+"js/validaciones/validations-base.js");
