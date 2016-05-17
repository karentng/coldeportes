form = '#form-formacion';
fields = {
    pais: {
        validators: {
            notEmpty: {
                message: 'Por favor escoja un país'
            }
        }
    },
    institucion: {
        validators: {
            notEmpty: {
                message: 'La institución de formación no puede ser vacía'
            }
        }
    },
    nivel: {
        validators: {
            notEmpty: {
                message: 'Por favor escoja un nivel'
            }
        }
    },
    estado: {
        validators: {
            notEmpty: {
                message: 'Por favor escoja un estado'
            },
        }
    },
    grado_semestre: {
        validators: {
            numeric: {
                message: 'El grado, año o semestre debe ser un numero'
            },
            greaterThan: {
                message: 'El grado,año o semestre no puede ser menor o igual a 0',
                value: 1

            }
        }
    },
    fecha_finalizacion: {
        validators: {
            numeric: {
                message: 'El año de finalización debe ser un numero'
            },
            greaterThan: {
                message: 'El año de finalización no puede ser menor o igual a 1950',
                value: 1950

            }
        }
    },
    soporte_cualificacion: {
        validators: {
            notEmpty: {
                message: 'El Soporte de cualificación y formación no puede ser vació'
            },
            file: {
                extension: 'pdf,jpeg,jpg,png',
                type: 'application/pdf,image/jpeg,image/png',
                maxSize: 5242880,   // 5120 * 1024,
                message: 'Por favor seleccione un archivo valido en formato pdf, jpg, o png no mayor a 5MB'
            }
        }
    }

};
$.getScript(base+"js/validaciones/validations-base.js");