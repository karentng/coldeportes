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
                    },
                    callback: {
                        message: 'La edad mínima debe ser menor a la máxima',
                        callback: function(fieldValue, validator){
                            var edad_max= parseInt($("#id_edad_maxima").val());
                            return parseInt(fieldValue) < edad_max
                        }
                    }
                }
            },
            edad_maxima: {
                validators: {
                    notEmpty: {
                        message: 'La edad máxima no puede ser vacía'
                    },
                    callback: {
                        message: 'La edad máxima debe ser mayor a la mínima',
                        callback: function(fieldValue, validator){
                            var edad_mi = parseInt($("#id_edad_minima").val());
                            return parseInt(fieldValue) > edad_mi;
                        }
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
    $("#id_edad_maxima").on('change',function(){
        $("#form-wizard-categorias").bootstrapValidator('revalidateField', 'edad_minima');
    });
    $("#id_edad_minima").on('change',function(){
        $("#form-wizard-categorias").bootstrapValidator('revalidateField', 'edad_maxima');
    });
});