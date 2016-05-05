$(document).ready(function() {
    var faIcon = {
        valid: 'fa fa-check-circle fa-lg text-success',
        invalid: 'fa fa-times-circle fa-lg',
        validating: 'fa fa-refresh'
    };

    $('#form-wizard-categorias').bootstrapValidator({
            feedbackIcons: faIcon,
            excluded: ':disabled',
            fields: {
            nombre_categoria: {
                validators: {
                    notEmpty: {
                        message: 'El nombre de la categoría no puede ser vacío'
                    }
                }
            },
            edad_minima: {
                validators: {
                    notEmpty: {
                        message: 'La edad mínima no puede ser vacía'
                    }
                }
            },
            edad_maxima: {
                validators: {
                    notEmpty: {
                        message: 'La edad máxima no puede ser vacía'
                    }
                }
            },
            descripcion: {
                validators: {
                    notEmpty: {
                        message: 'La descripción no puede ser vacía'
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