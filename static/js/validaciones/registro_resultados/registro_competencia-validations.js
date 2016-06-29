$(document).ready(function() {
    //Revalidar campos que usan plugins al ser actualizados
    

    var faIcon = {
        valid: 'fa fa-check-circle fa-lg text-success',
        invalid: 'fa fa-times-circle fa-lg',
        validating: 'fa fa-refresh'
    }

    $('#form-competencia').bootstrapValidator({
            feedbackIcons: faIcon,
            excluded: ':disabled',
            fields: {
                
                fecha_competencia: {
                    validators: {
                        notEmpty: {
                            message: 'La fecha de la competencia no puede ser vacía'
                        }
                    }
                },
                tipo_competencia: {
                    validators: {
                        notEmpty: {
                            message: 'Por favor seleccione un tipo de competencia'
                        }
                    }
                },
                tipo_registro: {
                    validators: {
                        notEmpty: {
                            message: 'Por favor seleccione un tipo de registro'
                        }
                    }
                },
                lugar: {
                    validators: {
                        notEmpty: {
                            message: 'Por favor escriba el lugar de la competencia'
                        }
                    }
                }, 
                tipos_participantes: {
                    validators: {
                        notEmpty: {
                            message: 'Por favor seleccione el tipo de participantes'
                        }
                    }
                }, 
                deporte: {
                    validators: {
                        notEmpty: {
                            message: 'Por favor seleccione un deporte'
                        }
                    }
                },            
            


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

        $("#id_fecha_competencia").on('change',function(e){
        $("#form-competencia").bootstrapValidator('revalidateField', 'fecha_competencia');
    });

});