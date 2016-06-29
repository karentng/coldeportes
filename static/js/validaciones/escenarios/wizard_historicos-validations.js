$(document).ready(function() {
    var faIcon = {
        valid: 'fa fa-check-circle fa-lg text-success',
        invalid: 'fa fa-times-circle fa-lg',
        validating: 'fa fa-refresh'
    }

    $('#form-wizard-historicos').bootstrapValidator({
            feedbackIcons: faIcon,
            excluded: ':disabled',
            fields: {
            fecha_inicio: {
                validators: {
                    notEmpty: {
                        message: 'La fecha de inicio no puede ser vacío'
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

    //Revalidar campos que usan plugins al ser actualizados
    $("#id_fecha_inicio").on('change',function(e){
        $("#form-wizard-historicos").bootstrapValidator('revalidateField', 'fecha_inicio');
    });
    
});