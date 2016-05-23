form = "#form-acudiente";
fields = {
    nombres: {
        validators: {
            notEmpty: {
                message: "El campo Nombres no puede ser vacío"
            }
        }
    },
    apellidos: {
        validators: {
            notEmpty: {
                message: "El campo Apellidos no puede ser vacío"
            }
        }
    },
    tipo_id: {
        validators: {
            notEmpty: {
                message: 'El tipo de indentificación no puede ser vacía'
            }
        }
    },
    identificacion: {
        validators: {
            notEmpty: {
                message: 'La identificación no puede ser vacía'
            }
        }
    },
    fecha_nacimiento: {
        validators: {
            notEmpty: {
                message: 'La fecha de nacimiento no puede ser vacía'
            },
            date: {
                message: 'El valor ingresado no es una fecha válida, debe ser menor al dia de hoy',
                format: 'YYYY-MM-DD',
                max: function(field, validator){
                    var d = new Date();

                    var curr_date = d.getDate();

                    var curr_month = d.getMonth() + 1;

                    var curr_year = d.getFullYear();
                    return curr_year + "-" + curr_month + "-" + curr_date;

                }
            }
        }
    },
    genero: {
        validators: {
            notEmpty: {
                message: 'El correo electrónico no puede ser vacío'
            }
        }
    },
    eps: {
        validators: {
            notEmpty: {
                message: 'El Sistema de salud afiliado no puede ser vacío'
            }
        }
    },
    soporte_id: {
        validators: {
            file: {
                extension: 'pdf,jpeg,jpg,png',
                type: 'application/pdf,image/jpeg,image/png',
                maxSize: 5242880,   // 5120 * 1024,
                message: 'Por favor seleccione un archivo valido en formato pdf, jpg, o png no mayor a 5MB'
            }
        }
    }
};



//Revalidar campos al ser actualizados
$("#id_fecha_nacimiento").on('change',function(e){
    $("#form-participante").bootstrapValidator('revalidateField', 'fecha_nacimiento');
});

$.getScript(base+"js/validaciones/validations-base.js");
