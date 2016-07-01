$(document).ready(function() {
    var faIcon = {
        valid: 'fa fa-check-circle fa-lg text-success',
        invalid: 'fa fa-times-circle fa-lg',
        validating: 'fa fa-refresh'
    };
    $.getScript(base+"plugins/moment/moment.min.js");
    $('#form-wizard-horarios').bootstrapValidator({
            feedbackIcons: faIcon,
            excluded: ':disabled',
            fields: {
            hora_inicio: {
                validators: {
                    notEmpty: {
                        message: 'La hora del inicio no puede ser vacío'
                    }
                }
            },
            hora_fin: {
                validators: {
                    notEmpty: {
                        message: 'La hora final no puede ser vacía'
                    },
                    callback:{
                        message: "El valor ingresado no es una hora válida, debe ser mayor a la hora de inicio",
                        callback: function(field, validator){
                            var inicio = $("input#id_hora_inicio").val();

                            var momento = new moment(field, 'HH:mm', true);
                            var momentInit = new moment(inicio, 'HH:mm', true);
                                console.log(field);
                            if (!momento.isValid()) {
                                console.log(momento);
                                return false;
                            }
                            return momento.isAfter(momentInit);

                        }
                    }
                }
            },
            dias: {
                validators: {
                    notEmpty: {
                        message: 'Los días no pueden ser vacíos'
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
    var $formWizard = $("#form-wizard-horarios");
    $("#id_hora_inicio").on('change',function(e){
        $formWizard.bootstrapValidator('revalidateField', 'hora_inicio');
        $formWizard.bootstrapValidator('revalidateField', 'hora_fin');
    });
    $("#id_hora_fin").on('change',function(e){
        $formWizard.bootstrapValidator('revalidateField', 'hora_inicio');
        $formWizard.bootstrapValidator('revalidateField', 'hora_fin');
    });
});