form = "#form-wizard-identificacion";
fields = {
    tipo_identificacion: {
        validators: {
            notEmpty: {
                message: 'Debe de seleccionar un tipo de identificación para el dirigente'
            }
        }
    },
    identificacion: {
        validators: {
            notEmpty: {
                message: 'La identificación del dirigente no puede ser vacía'
            },
            numeric: {
                message: 'El número de identificación solo puede contener números'
            }
        }
    },
    nombres: {
        validators: {
            notEmpty: {
                message: 'Los nombres del dirigente no puedes ser vacíos'
            }
        }
    },
    apellidos: {
        validators: {
            notEmpty: {
                message: 'Los apellidos del dirigente no pueden ser vacíos'
            }
        }
    },
    genero: {
        validators: {
            notEmpty: {
                message: 'Debe de seleccionar un género para el dirigente'
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
    nacionalidad: {
        validators: {
            notEmpty: {
                message: 'Debe de seleccione al menos una nacionalidad para el dirigente'
            }
        }
    },
    foto: {
        validators: {
            file: {
                extension: 'png,jpg,jpeg,svg',
                message: 'Seleccione una imagen con alguno de los siguientes formatos (png, jpg, jpeg, svg)',
                maxSize: 5242880 //5MB
            }
        }
    },
    perfil: {
        validators: {
            notEmpty: {
                message: 'El perfil del dirigente no puede ser vacío'
            }
        }
    },
    
};
$.getScript(base+"js/validaciones/validations-base.js");