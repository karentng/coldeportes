form = "#wizard-caf-validations";
fields = {
    nombre: {
        validators: {
            notEmpty: {
                message: 'El nombre no puede ser vacío'
            }
        }
    },
    direccion: {
        validators: {
            notEmpty: {
                message: 'La dirección no puede ser vacía'
            }
        }
    },
    telefono: {
        validators: {
            notEmpty: {
                message: 'El teléfono no puede ser vacío'
            }
        }
    },
    email: {
        validators: {
            notEmpty: {
                message: 'El email no puede ser vacío'
            },
            emailAddress: {
                message: 'El valor ingresado no es un correo electrónico válido'
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
    latitud: {
        validators: {
            notEmpty: {
                message: 'La latitud no puede ser vacía'
            },
            numeric: {
                message: 'Por favor ingrese valores numéricos'
            },
        }
    },
    longitud: {
        validators: {
            notEmpty: {
                message: 'La longitud no puede ser vacía'
            },
            numeric: {
                message: 'Por favor ingrese valores numéricos'
            },
        }
    },
    altura: {
        validators: {
            notEmpty: {
                message: 'La altura no puede ser vacía'
            },
            integer: {
                message: 'Por favor ingrese valores enteros'
            },
            greaterThan:{
                message: 'Por favor ingrese valores mayores o iguales a 0'
            }
        }
    },
    web: {
        validators: {
            uri: {
                message: 'Ingrese una URL válida (Ej: http://google.com.co)'
            }
        }
    }

};
$.getScript(base+"js/validaciones/validations-base.js");