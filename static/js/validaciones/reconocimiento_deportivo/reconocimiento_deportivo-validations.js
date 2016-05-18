$(document).ready(function() {
    //Revalidar campos que usan plugins al ser actualizados
    

    var faIcon = {
        valid: 'fa fa-check-circle fa-lg text-success',
        invalid: 'fa fa-times-circle fa-lg',
        validating: 'fa fa-refresh'
    }

    $('#form-reconocimiento-deportivo').bootstrapValidator({
            feedbackIcons: faIcon,
            excluded: ':disabled',
            fields: {
                para_quien: {
                    validators: {
                        notEmpty: {
                            message: 'Por favor seleccione una entidad'
                        }
                    }
                },
                tipo: {
                    validators: {
                        notEmpty: {
                            message: 'Por favor seleccione un tipo'
                        }
                    }
                },
                descripcion: {
                    validators: {
                        notEmpty: {
                            message: 'Debe describir la solicitud'
                        },
                        stringLength: {
                            message: 'El tamaño de la descripción debe tener como maximo 500 caracteres',
                            max: 500
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
                id_solicitante: {
                    validators: {
                        notEmpty: {
                            message: 'La identificación no puede ser vacía'
                        },
                        integer: {
                            message: 'Por favor ingrese valores numéricos'
                        },
                    }
                }, 
                tel_solicitante: {
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
                vinculo_solicitante: {
                    validators: {
                        notEmpty: {
                            message: 'Por favor seleccione el vínculo con la entidad'
                        }
                    }
                },
                archivo: {
                    validators:{
                        file: {
                            extension: 'pdf, PDF, png, PNG, jpg, JPEG',
                            message: 'Seleccione una imagen con alguno de los siguientes formatos (pdf, png, jpg, JPEG) cuyo tamaño sea menor a 5MB',
                            maxSize: 5242880,
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

        $("#id_fecha_competencia").on('change',function(e){
        $("#form-competencia").bootstrapValidator('revalidateField', 'fecha_competencia');
    });

});