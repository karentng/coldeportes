form = "#form-preinscrito";
fields = {
    nombre: {
        validators: {
            notEmpty: {
                message: "El campo Nombres no puede ser vacío"
            }
        }
    },
    apellido: {
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
    email: {
        validators: {
            notEmpty: {
                message: 'El correo electrónico no puede ser vacío'
            },
            emailAddress: {
                message: 'El valor ingresado no es un correo válido'
            }
        }
    },
    confirmacion_mail: {
        validators:{
            emailAddress: {
                message: 'El valor ingresado no es un correo válido'
            },
            callback:{
                message: "Los correos electrónicos no coinciden",
                callback: function(value, validator){

                    return value == $("#id_email").val();
                }
            }

        }
    }
};



//Revalidar campos al ser actualizados
$("#id_fecha_nacimiento").on('change',function(e){
    $("#form-preinscrito").bootstrapValidator('revalidateField', 'fecha_nacimiento');
});

$.getScript(base+"js/validaciones/validations-base.js");
