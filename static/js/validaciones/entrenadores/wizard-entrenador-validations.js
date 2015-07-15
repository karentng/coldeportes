$(document).ready(function() {
    var faIcon = {
        valid: 'fa fa-check-circle fa-lg text-success',
        invalid: 'fa fa-times-circle fa-lg',
        validating: 'fa fa-refresh'
    }

    $('#form-wizard-entrenador').bootstrapValidator({
            feedbackIcons: faIcon,
            excluded: ':disabled',
            fields: {
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
                        callback: {
                            message: 'Escoja al menos una nacionalidad',
                            callback: function(value, validator, $field) {
                                // Get the selected options

                                var options = validator.getFieldElements('nacionalidad').val();
                                return (options != null && options.length > 0);
                            }
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
            },


            }
        }).on('success.field.bv', function(e, data) {
            // $(e.target)  --> The field element
            // data.bv      --> The BootstrapValidator instance
            // data.field   --> The field name
            // data.element --> The field element

            var $parent = data.element.parents('.form-group');

            // Remove the has-success class
            $parent.removeClass('has-success');
        });

    //Revalidar campos que usan plugins al ser actualizados
    $("#id_fecha_nacimiento").on('change',function(e){
        $("#form-wizard-entrenador").bootstrapValidator('revalidateField', 'fecha_nacimiento');
    });
});