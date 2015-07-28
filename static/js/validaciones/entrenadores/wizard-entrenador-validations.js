form = "#form-wizard-entrenador";
fields = {
            nombres: {
                validators: {
                    notEmpty: {
                        message: 'El nombre del entrenador no puede ser vacío'
                    }
                }
            },
            apellidos: {
                validators: {
                    notEmpty: {
                        message: 'Los apellidos del entrenador no pueden ser vacíos'
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
                        message: 'Seleccione una imagen con alguno de los siguientes formatos (png, jpg, jpeg, svg)'
                    }
                }
            },
            nro_id: {
                validators: {
                    notEmpty: {
                        message: 'El número de identificación no puede ser vacío'
                    },
                    numeric: {
                        message: 'El número de identificación solo puede contener números'
                    },
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
                        format: 'YYYY-MM-DD'
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
            altura: {
                validators: {
                    numeric: {
                        message: 'La altura solo puede contener números'
                    }
                }
            },
            peso: {
                validators: {
                    numeric: {
                        message: 'El peso solo puede contener números'
                    }
                }
            }


        };
//Revalidar campos al ser actualizados
    $("#id_fecha_nacimiento").on('change',function(e){
        $(form).bootstrapValidator('revalidateField', 'fecha_nacimiento');
    });
$.getScript(base+"js/validaciones/validations-base.js");

