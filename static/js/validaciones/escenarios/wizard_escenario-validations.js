$(document).ready(function() {
    //Revalidar campos que usan plugins al ser actualizados
    

    var faIcon = {
        valid: 'fa fa-check-circle fa-lg text-success',
        invalid: 'fa fa-times-circle fa-lg',
        validating: 'fa fa-refresh'
    }

    $('#form-wizard-escenarios').bootstrapValidator({
            feedbackIcons: faIcon,
            excluded: ':disabled',
            fields: {
            nombre: {
                validators: {
                    notEmpty: {
                        message: 'El nombre del escenario no puede ser vacío'
                    }
                }
            },
            direccion: {
                validators: {
                    notEmpty: {
                        message: 'La dirección del escenario no puede ser vacía'
                    }
                }
            },
            latitud: {
                validators: {
                    notEmpty: {
                        message: 'La latitud del escenario no puede ser vacía'
                    },
                    numeric: {
                        message: 'La latitud sólo puede contener números'
                    },
                }
            },
            longitud: {
                validators: {
                    notEmpty: {
                        message: 'La longitud del escenario no puede ser vacía'
                    },
                    numeric: {
                        message: 'La longitud del escenario sólo puede contener números'
                    },
                }
            },
            altura: {
                validators: {
                    notEmpty: {
                        message: 'La altura del escenario no puede ser vacía'
                    },
                    integer: {
                        message: 'Por favor ingrese valores enteros'
                    },
                    greaterThan:{
                        message: 'Por favor ingrese valores mayores o iguales a 0'
                    }
                }
            },
            comuna: {
                validators: {
                    notEmpty: {
                        message: 'La comuna del escenario no puede ser vacía'
                    },
                    integer: {
                        message: 'Por favor ingrese valores enteros'
                    },
                    greaterThan:{
                        message: 'Por favor ingrese valores enteros mayores o iguales a 0'
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
            estrato: {
                validators: {
                    notEmpty: {
                        message: 'El estrato del escenario no puede ser vacío'
                    }
                }
            },   
            barrio: {
                validators: {
                    notEmpty: {
                        message: 'El barrio del escenario no puede ser vacío'
                    }
                }
            },   
            nombre_administrador: {
                validators: {
                    notEmpty: {
                        message: 'El nombre del administrador del escenario no puede ser vacío'
                    }
                }
            },    
            capacidad_espectadores: {
                validators: {
                    notEmpty: {
                        message: 'La capacidad de espectadores del escenario no puede ser vacío'
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

});