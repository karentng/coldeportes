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
            }
        }
    },
    longitud: {
        validators: {
            notEmpty: {
                message: 'La longitud no puede ser vacía'
            }
        }
    },
    altura: {
        validators: {
            notEmpty: {
                message: 'La altura no puede ser vacía'
            }
        }
    },
    nombre_administrador: {
        validators: {
            notEmpty: {
                message: 'El nombre del administrador no puede ser vacío'
            }
        }
    },
    web: {
        validators: {
            uri: {
                message: 'La página web no es válida'
            }
        }
    }

};
$.getScript(base+"js/validaciones/validations-base.js");