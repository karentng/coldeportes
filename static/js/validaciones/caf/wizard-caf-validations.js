$(document).ready(function() {
    var faIcon = {
        valid: 'fa fa-check-circle fa-lg text-success',
        invalid: 'fa fa-times-circle fa-lg',
        validating: 'fa fa-refresh'
    }

    $('#wizard-caf-validations').bootstrapValidator({
            feedbackIcons: faIcon,
            excluded: ':disabled',
            fields: {
                nombre: {
                    validators: {
                        notEmpty: {
                            message: 'El nombre no puede ser vacío'
                        }
                    }
                },
                direccion: {
                    validators: {
                        notEmpty: {
                            message: 'La dirección no puede ser vacía'
                        }
                    }
                },
                telefono: {
                    validators: {
                        notEmpty: {
                            message: 'El teléfono no puede ser vacío'
                        }
                    }
                },
                email: {
                    validators: {
                        notEmpty: {
                            message: 'El email no puede ser vacío'
                        },
                        emailAddress: {
                            message: 'El valor ingresado no es un correo electrónico válido'
                        }
                    }
                },
                ciudad: {
                    validators: {
                        notEmpty: {
                            message: 'Por favor seleccione una ciudad'
                        }
                    }
                },
                comuna: {
                    validators: {
                        notEmpty: {
                            message: 'La comuna no puede ser vacía'
                        }
                    }
                },
                barrio: {
                    validators: {
                        notEmpty: {
                            message: 'El barrio no puede ser vacío'
                        }
                    }
                },
                estrato: {
                    validators: {
                        notEmpty: {
                            message: 'Por favor seleccione un estrato'
                        }
                    }
                },
                latitud: {
                    validators: {
                        notEmpty: {
                            message: 'La latitud no puede ser vacía'
                        }
                    }
                },
                longitud: {
                    validators: {
                        notEmpty: {
                            message: 'La longitud no puede ser vacía'
                        }
                    }
                },
                altura: {
                    validators: {
                        notEmpty: {
                            message: 'La altura no puede ser vacía'
                        }
                    }
                },
                nombre_administrador: {
                    validators: {
                        notEmpty: {
                            message: 'El nombre del administrador no puede ser vacío'
                        }
                    }
                }

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
});