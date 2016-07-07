form = "#form-wizard-personal-apoyo";
fields = {
            nombres: {
                validators: {
                    notEmpty: {
                        message: 'El nombre no puede ser vacío'
                    }
                }
            },
            apellidos: {
                validators: {
                    notEmpty: {
                        message: 'Los apellidos no pueden ser vacíos'
                    }
                }
            },
            genero: {
                validators: {
                    notEmpty: {
                        message: 'Por favor escoja un género'
                    }
                }
            },
            foto: {
                validators: {
                    file: {
                        extension: 'png,jpg,jpeg,svg',
                        message: 'Seleccione una imagen con alguno de los siguientes formatos (png, jpg, jpeg, svg) cuyo tamaño sea menor a 5MB',
                        maxSize: 5242880, // 5MB: http://www.beesky.com/newsite/bit_byte.htm
                    }
                }
            },
            identificacion: {
                validators: {
                    notEmpty: {
                        message: 'El número de identificación no puede ser vacío'
                    },
                    regexp: {
                        regexp: "^[0-9a-zA-Z]+$",
                        message: 'El número de identificación solo puede contener números ó letras'
                    }
                }
            },
            correo_electronico: {
                validators: {
                    emailAddress: {
					    message: 'El valor ingresado no es un correo electrónico válido'
				    }
                }
            },
            fecha_nacimiento: {
                validators: {
                    notEmpty: {
                        message: 'La fecha de nacimiento no puede ser vacía'
                    },
                    date: {
					    message: 'El valor ingresado no es una fecha válida',
                        format: 'YYYY-MM-DD',
                        message: 'La fecha de nacimiento no puede ser mayor a hoy',
                        max: ($.datepicker.formatDate('yy-mm-dd', new Date())).toString()
				    }
                }
            },
            nacionalidad: {
                validators: {
                    notEmpty: {
                      message:"Escoja almenos una nacionalidad"
                    }
                }
            },
            ciudad: {
                    validators: {
                        notEmpty: {
                        message: 'Por favor escoja una ciudad'
                        }
                    }
            },
            soporte_identificacion: {
                validators: {
                    notEmpty: {
                        message: 'El soporte de identificación no puede ser vacío'
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
//Revalidar campos al ser actualizados
    $("#id_fecha_nacimiento").on('change',function(e){
        $(form).bootstrapValidator('revalidateField', 'fecha_nacimiento');
    });
$.getScript(base+"js/validaciones/validations-base.js");

