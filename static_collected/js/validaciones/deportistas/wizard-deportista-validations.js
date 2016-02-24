form = "#form-wizard-deportista";
fields = {
            nombres: {
                validators: {
                    notEmpty: {
                        message: 'El nombre del deportista no puede ser vacío'
                    }
                }
            },
            apellidos: {
                validators: {
                    notEmpty: {
                        message: 'Los apellidos del deportista no pueden ser vacíos'
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
            tipo_id: {
                validators: {
                    notEmpty: {
                        message: 'Por favor escoja un tipo de identificación'
                    },
                }
            },
            identificacion: {
                validators: {
                    notEmpty: {
                        message: 'El número de identificación no puede ser vacío'
                    },
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
            ciudad_residencia: {
                    validators: {
                        notEmpty: {
                        message: 'Por favor escoja una ciudad'
                        }
                    }
            },
            barrio: {
                validators: {
                    notEmpty: {
                        message: 'El barrio del deportista no puede ser vacío'
                    }
                }
            },
            comuna: {
                validators: {
                    notEmpty: {
                        message: 'La comuna del deportista no puede ser vacía'
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
            telefono: {
                validators: {
                    notEmpty: {
                        message: 'El telefono no puede ser vacío'
                    }
                }
            },
            direccion: {
                validators: {
                    notEmpty: {
                        message: 'La direccion no puede ser vacía'
                    }
                }
            },
            disciplinas: {
                    validators: {
                        notEmpty: {
                        message: 'Por favor escoja al menos una disciplina'
                        }
                    }
            },
            video: {
                validators: {
                    url: {
                        message: 'Esta no es una url valida'
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
            }

        };
//Revalidar campos al ser actualizados
    $("#id_fecha_nacimiento").on('change',function(e){
        $(form).bootstrapValidator('revalidateField', 'fecha_nacimiento');
    });
$.getScript(base+"js/validaciones/validations-base.js");
