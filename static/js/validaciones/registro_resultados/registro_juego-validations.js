$(document).ready(function() {
    //Revalidar campos que usan plugins al ser actualizados
    

    var faIcon = {
        valid: 'fa fa-check-circle fa-lg text-success',
        invalid: 'fa fa-times-circle fa-lg',
        validating: 'fa fa-refresh'
    }

    $('#form-juego').bootstrapValidator({
            feedbackIcons: faIcon,
            excluded: ':disabled',
            fields: {
                nombre: {
                    validators: {
                        notEmpty: {
                            message: 'El nombre del juego no puede ser vacío'
                        }
                    }
                },
                anio: {
                    validators: {
                        notEmpty: {
                            message: 'El año no puede ser vacío'
                        },
                        integer: {
                            message: 'Por favor ingrese valores enteros'
                        },
                        greaterThan:{
                            message: 'Por favor ingrese valores enteros mayores o iguales a 0'
                        }
                    }
                },
                pais: {
                    validators: {
                        notEmpty: {
                            message: 'Por favor seleccione un país'
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

});