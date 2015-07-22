form = "#form-wizard-identificacion";
fields = {
    tipo_identificacion: {
        validators: {
            notEmpty: {
                message: 'El tipo de identificación del dirigente no puede ser vacío'
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
                message: 'Por favor selecciones un género'
            }
        }
    },
    cargo: {
        validators: {
            notEmpty: {
                message: 'El cargo del dirigente no puede ser vacío'
            }
        }
    },
    telefono: {
        validators: {
            notEmpty: {
                message: 'El teléfono del dirigente no puede ser vacío'
            },
            numeric: {
                message: 'El teléfono solo puede contener números'
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
                message: 'Por favor seleccione al menos una nacionalidad para el dirigente'
            }
        }
    },
    fecha_posesion: {
        validators: {
            notEmpty: {
                message: 'La fecha de posesión del dirigente no puede ser vacía'
            },
            date: {
                message: 'El valor ingresado no es una fecha válida',
                format: 'YYYY-MM-DD',
                max: 'fecha_retiro'
            }
        }
    },
    fecha_retiro: {
        validators: {
            date: {
                message: 'El valor ingresado no es una fecha válida',
                format: 'YYYY-MM-DD',
                min: 'fecha_posesion'
            }
        }
    },
    foto: {
        validators: {
            file: {
                extension: 'png,jpg,jpeg,svg',
                message: 'Seleccione una imagen con alguno de los siguientes formatos (png, jpg, jpeg, svg)'
            }
        }
    },
    descripcion: {
        validators: {
            notEmpty: {
                message: 'Descripción y/o logros del dirigente no puede ser vacío'
            }
        }
    },
    
};
//Revalidar campos al ser actualizados
$("#id_fecha_posesion").on('change',function(e){
    $("#form-wizard-identificacion").bootstrapValidator('revalidateField', 'fecha_posesion');
});
$("#id_fecha_retiro").on('change',function(e){
    $("#form-wizard-identificacion").bootstrapValidator('revalidateField', 'fecha_retiro');
});
$.getScript(base+"js/validaciones/validations-base.js");