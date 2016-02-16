form = "#entidad";
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
    disciplina: {
        validators: {
            notEmpty: {
                message: 'Por favor seleccione una disciplina'
            }
        }
    },
    departamento: {
        validators: {
            notEmpty: {
                message: 'Por favor seleccione un departamento'
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
    pagina: {
        validators: {
            notEmpty: {
                message: 'La página no puede ser vacía'
            }
        }
    },
    pagina_web: {
        validators: {
            uri: {
                message: 'Ingrese una URL válida (Ej: http://google.com.co)'
            }
        }
    },
};
$.getScript(base+"js/validaciones/validations-base.js");