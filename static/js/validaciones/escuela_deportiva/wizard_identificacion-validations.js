form = "#form-wizard-identificacion";
fields = {
    nombre: {
        validators: {
            notEmpty: {
                message: 'El nombre de la Escuela de Formación Deportiva no puede ser vacío'
            }
        }
    },
    email: {
        validators: {
            emailAddress: {
                message: 'El valor ingresado no es un correo electrónico válido'
            }
        }
    },
    telefono_fijo: {
        validators: {
            notEmpty: {
                message: 'El teléfono de la Escuela de Formación Deportiva no puede ser vacío'
            }
        }
    },
    direccion: {
        validators: {
            notEmpty: {
                message: 'La dirección de la Escuela de Formación Deportiva no puede ser vacío'
            }
        }
    },
    ciudad: {
        validators: {
            notEmpty: {
                message: 'Por favor seleccione una ciudad'
            }
        }
    },
    comuna: {
        validators: {
            notEmpty: {
                message: 'La comuna no puede ser vacía'
            },
            integer: {
                message: 'Por favor ingrese valores enteros'
            },
            greaterThan:{
                message: 'Por favor ingrese valores enteros mayores o iguales a 0'
            }
        }
    },
    barrio: {
        validators: {
            notEmpty: {
                message: 'El barrio no puede ser vacío'
            }
        }
    },
    estrato: {
        validators: {
            notEmpty: {
                message: 'Por favor seleccione un estrato'
            }
        }
    },
    aval: {
        validators: {
            file: {
                extension: 'pdf',
                message: 'Selecciones un archivo en formato pdf de máximo 5MB',
                maxSize: 5242880 //5MB
            }
        }
    }
};
$.getScript(base+"js/validaciones/validations-base.js");