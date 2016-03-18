$(document).ready(function() {
    var faIcon = {
        valid: 'fa fa-check-circle fa-lg text-success',
        invalid: 'fa fa-times-circle fa-lg',
        validating: 'fa fa-refresh'
    }

    $('#form-wizard-videos').bootstrapValidator({
            feedbackIcons: faIcon,
            excluded: ':disabled',
            fields: {
            url: {
                validators: {
                    notEmpty: {
                        message: 'La url del video del escenario no puede ser vacío'
                    }
                }
            },
            descripcion_video: {
                validators: {
                    notEmpty: {
                        message: 'La descripción del video del escenario no puede ser vacía'
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