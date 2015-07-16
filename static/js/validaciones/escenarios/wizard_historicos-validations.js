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
                        message: 'La fecha de inicio del dato histórico del escenario no puede ser vacío'
                    }
                }
            },
            fecha_fin: {
                validators: {
                    notEmpty: {
                        message: 'La fecha final del dato histórico del escenario no puede ser vacía'
                    }
                }
            },
            descripcion: {
                validators: {
                    notEmpty: {
                        message: 'La descripción del dato histórico del escenario no puede ser vacía'
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
    $("#id_fecha_fin").on('change',function(e){
        $("#form-wizard-historicos").bootstrapValidator('revalidateField', 'fecha_fin');
    });
});