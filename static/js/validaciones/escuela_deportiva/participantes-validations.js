form = "#form-participante";
$.getScript(base+"plugins/moment/moment.min.js");
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
                format: 'YYYY-MM-DD'
            },
            callback:{
                message: "El valor ingresado no es una fecha válida, debe ser menor al dia de hoy",
                callback: function(field, validator){
                    var d = new Date();
                    var curr_date = d.getDate();
                    var curr_month = d.getMonth() + 1;
                    var curr_year = d.getFullYear();
                    var today = curr_year + "-" + curr_month + "-" + curr_date;

                    var momento = new moment(field, 'YYYY-MM-DD', true);
                    if (!momento.isValid()) {
                        return false;
                    }
                    return momento.isBefore(today);

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
    ciudad_residencia: {
        validators: {
            notEmpty: {
                message: 'La ciudad de residencia no puede ser vacía'
            }
        }
    },
    institucion_educativa: {
        validators: {
            notEmpty: {
                message: 'La Institución educativa no puede ser vacía'
            }
        }
    },
    anho_curso: {
        validators: {
            notEmpty: {
                message: 'El Año del curso no puede ser vacío'
            }
        }
    },
    telefono: {
        validators: {
            notEmpty: {
                message: 'El Telefono no puede ser vacío'
            }
        }
    },
    direccion: {
        validators: {
            notEmpty: {
                message: 'La Dirección no puede ser vacía'
            }
        }
    },
    nacionalidad: {
        validators: {
            notEmpty: {
                message: 'La Nacionalidad no puede ser vacía'
            }
        }
    },
    eps: {
        validators: {
            notEmpty: {
                message: 'El Sistema de salud afiliado no puede ser vacío'
            }
        }
    }
};



//Revalidar campos al ser actualizados
$("#id_fecha_nacimiento").on('change',function(e){
    $("#form-participante").bootstrapValidator('revalidateField', 'fecha_nacimiento');
});

$.getScript(base+"js/validaciones/validations-base.js");
