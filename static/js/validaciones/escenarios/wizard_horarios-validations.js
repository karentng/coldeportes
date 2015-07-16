$(document).ready(function() {
    var faIcon = {
        valid: 'fa fa-check-circle fa-lg text-success',
        invalid: 'fa fa-times-circle fa-lg',
        validating: 'fa fa-refresh'
    }

    $('#form-wizard-horarios').bootstrapValidator({
            feedbackIcons: faIcon,
            excluded: ':disabled',
            fields: {
            hora_inicio: {
                validators: {
                    notEmpty: {
                        message: 'La hora del inicio del horario del escenario no puede ser vacío'
                    }
                }
            },
            hora_fin: {
                validators: {
                    notEmpty: {
                        message: 'La hora final del horario del escenario no puede ser vacía'
                    }
                }
            },
            dias: {
                validators: {
                    notEmpty: {
                        message: 'Los días del horario del escenario no pueden ser vacíos'
                    }
                }
            },
            descripcion: {
                validators: {
                    notEmpty: {
                        message: 'La descripción del horario del escenario no puede ser vacía'
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
    $("#id_hora_inicio").on('change',function(e){
        $("#form-wizard-horarios").bootstrapValidator('revalidateField', 'hora_inicio');
    });
    $("#id_hora_fin").on('change',function(e){
        $("#form-wizard-horarios").bootstrapValidator('revalidateField', 'hora_fin');
    });
});