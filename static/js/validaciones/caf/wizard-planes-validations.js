form = "#wizard-planes-validations";
fields = {
    nombre: {
        validators: {
            notEmpty: {
                message: 'El nombre no puede ser vacío'
            }
        }
    },
    precio: {
        validators: {
            notEmpty: {
                message: 'El precio no puede ser vacío'
            }
        }
    },
    descripcion: {
        validators: {
            notEmpty: {
                message: 'La descripción no puede ser vacía'
            }
        }
    }
};
$.getScript(base+"js/validaciones/validations-base.js");