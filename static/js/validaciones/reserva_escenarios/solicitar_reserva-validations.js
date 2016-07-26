$(document).ready(function() {
    //Revalidar campos que usan plugins al ser actualizados
    

    var faIcon = {
        valid: 'fa fa-check-circle fa-lg text-success',
        invalid: 'fa fa-times-circle fa-lg',
        validating: 'fa fa-refresh'
    }

    $('#form-reserva-escenario').bootstrapValidator({
            feedbackIcons: faIcon,
            excluded: ':disabled',
            fields: {
                nombre_equipo: {
                    validators: {
                        notEmpty: {
                            message: 'El nombre del solicitante del reconocimiento deportivo no puede ser vacío'
                        }
                    }
                }, 
                nombre_solicitante: {
                    validators: {
                        notEmpty: {
                            message: 'El nombre del solicitante del reconocimiento deportivo no puede ser vacío'
                        }
                    }
                },                     
                identificacion_solicitante: {
                    validators: {
                        notEmpty: {
                            message: 'La identificación no puede ser vacía'
                        },
                        integer: {
                            message: 'Por favor ingrese valores numéricos'
                        },
                    }
                }, 
                telefono_solicitante: {
                    validators: {
                        notEmpty: {
                            message: 'Por favor ingrese un teléfono'
                        },
                        integer: {
                            message: 'Por favor ingrese valores numéricos'
                        },
                    }
                }, 
                direccion_solicitante: {
                    validators: {
                        notEmpty: {
                            message: 'Por favor ingrese una dirección'
                        }
                    }
                },
                descripcion: {
                    validators: {
                        notEmpty: {
                            message: 'Por favor de una descripción del evento a realizar'
                        },
                        stringLength: {
                            message: 'El tamaño de la descripción debe tener como maximo 500 caracteres',
                            max: 500
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

        $("#id_fecha_competencia").on('change',function(e){
        $("#form-competencia").bootstrapValidator('revalidateField', 'fecha_competencia');
    });

});