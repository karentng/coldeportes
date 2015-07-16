$(document).ready(function() {
    var faIcon = {
        valid: 'fa fa-check-circle fa-lg text-success',
        invalid: 'fa fa-times-circle fa-lg',
        validating: 'fa fa-refresh'
    }

    $('#wizard-planes-validations').bootstrapValidator({
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
                precio: {
                    validators: {
                        notEmpty: {
                            message: 'El precio no puede ser vacío'
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