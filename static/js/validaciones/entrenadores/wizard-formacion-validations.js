$(document).ready(function() {
    var faIcon = {
        valid: 'fa fa-check-circle fa-lg text-success',
        invalid: 'fa fa-times-circle fa-lg',
        validating: 'fa fa-refresh'
    }

    $('#form-formacion').bootstrapValidator({
            feedbackIcons: faIcon,
            excluded: ':disabled',
            fields: {
            disciplina_deportiva: {
                    validators: {
                        callback: {
                            message: 'Escoja al menos una disciplina deportiva',
                            callback: function(value, validator, $field) {
                                // Get the selected options

                                var options = validator.getFieldElements('disciplina_deportiva').val();
                                return (options != null && options.length > 0);
                            }
                        }
                    }
            },
            denominacion_diploma: {
                validators: {
                    notEmpty: {
                        message: 'La denominación del diploma no puede ser vacía'
                    }
                }
            },
            nivel: {
                validators: {
                    notEmpty: {
                        message: 'El nivel no puede ser vacío'
                    }
                }
            },
            institucion_formacion: {
                validators: {
                    notEmpty: {
                        message: 'La institución de formación no puede ser vacía'
                    }
                }
            },
            pais_formacion: {
                    validators: {
                        notEmpty: {
                        message: 'Por favor escoja un país'
                        }
                    }
            },
            fecha_comienzo: {
                validators: {
                    notEmpty: {
                        message: 'La fecha de inicio no puede ser vacía'
                    },
                    date: {
					    message: 'El valor ingresado no es una fecha válida',
                        format: 'YYYY-MM-DD',
                        max: 'fecha_fin'
				    }
                }
            },
            fecha_fin: {
                validators: {
                    date: {
					    message: 'El valor ingresado no es una fecha válida',
                        format: 'YYYY-MM-DD',
                        max: 'fecha_comienzo'
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