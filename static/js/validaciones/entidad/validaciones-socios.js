/**
 * Created by diegoamt on 3/03/16.
 */

form = "#formulario-socio";
fields = {
    nombre: {
        validators: {
            notEmpty: {
                message: "El nombre no puede ser vacío"
            }
        }
    },
    apellido: {
        validators: {
            notEmpty: {
                message: "El apellido no puede ser vacío"
            }
        }
    },
    tipo_documento: {
        validators: {
            notEmpty: {
                message: "El tipo de documento no puede ser vacío"
            }
        }
    },
    numero_documento: {
        validators: {
            notEmpty: {
                message: "El número de documento no puede ser vacío"
            },
            regexp: {
                regexp: "^[0-9a-zA-Z]+$",
                message: "El número de documento solo puede contener números ó letras"
            }
        }
    },
    correo: {
        validators: {
            emailAddress: {
                message: "La dirección de correo electrónico no es válida"
            }
        }
    },
    ciudad: {
        validators: {
            notEmpty: {
                message: "La ciudad no puede ser vacía"
            }
        }
    }
};
$.getScript(base+"js/validaciones/validations-base.js");