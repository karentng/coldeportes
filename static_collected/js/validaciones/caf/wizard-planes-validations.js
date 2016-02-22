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
            },
            integer: {
                message: 'Por favor ingrese valores enteros'
            },
            greaterThan:{
                message: 'Por favor ingrese valores mayores o iguales a 0'
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