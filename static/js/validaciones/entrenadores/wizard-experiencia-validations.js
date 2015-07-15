$(document).ready(function() {
    var faIcon = {
        valid: 'fa fa-check-circle fa-lg text-success',
        invalid: 'fa fa-times-circle fa-lg',
        validating: 'fa fa-refresh'
    }

    $('#form-experiencia').bootstrapValidator({
            feedbackIcons: faIcon,
            excluded: ':disabled',
            fields: {
            nombre_cargo: {
                validators: {
                    notEmpty: {
                        message: 'El nombre del cargo no puede ser vacío'
                    }
                }
            },
            institucion: {
                validators: {
                    notEmpty: {
                        message: 'La institución no puede ser vacía'
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