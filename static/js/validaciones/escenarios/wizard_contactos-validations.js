$(document).ready(function() {
    var faIcon = {
        valid: 'fa fa-check-circle fa-lg text-success',
        invalid: 'fa fa-times-circle fa-lg',
        validating: 'fa fa-refresh'
    }

    $('#form-wizard-contactos').bootstrapValidator({
            feedbackIcons: faIcon,
            excluded: ':disabled',
            fields: {
            nombre: {
                validators: {
                    notEmpty: {
                        message: 'El nombre  del contacto del escenario no puede ser vacío'
                    }
                }
            },
            telefono: {
                validators: {
                    notEmpty: {
                        message: 'El telefono del contacto del escenario no puede ser vacío'
                    }
                }
            },
            email: {
                validators: {
                    emailAddress: {
                        message: 'El valor ingresado no es un correo electrónico válido'
                    }
                }
            },
            descripcion: {
                validators: {
                    notEmpty: {
                        message: 'La descripción del contacto del escenario no puede ser vacía'
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