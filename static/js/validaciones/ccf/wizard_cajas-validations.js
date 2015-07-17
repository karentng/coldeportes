$(document).ready(function() {
    var faIcon = {
        valid: 'fa fa-check-circle fa-lg text-success',
        invalid: 'fa fa-times-circle fa-lg',
        validating: 'fa fa-refresh'
    }

    $('#form-wizard-cajas').bootstrapValidator({
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
            clasificacion: {
                validators: {
                    notEmpty: {
                        message: 'Por favor seleccione una clasificación'
                    }
                }
            },
            region: {
                validators: {
                    notEmpty: {
                        message: 'Por favor seleccione una región'
                    }
                }
            },
            infraestructura: {
                validators: {
                    notEmpty: {
                        message: 'Por favor seleccione la infraestructura'
                    }
                }
            },
            publico: {
                validators: {
                    notEmpty: {
                        message: 'Por favor seleccione el público'
                    }
                }
            },
            servicios: {
                validators: {
                    notEmpty: {
                        message: 'Por favor seleccione los servicios'
                    }
                }
            },
            tipo_institucion: {
                validators: {
                    notEmpty: {
                        message: 'Por favor seleccione el tipo de institución'
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