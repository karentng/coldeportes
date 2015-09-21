$(document).ready(function() {
    //Revalidar campos que usan plugins al ser actualizados
    

    var faIcon = {
        valid: 'fa fa-check-circle fa-lg text-success',
        invalid: 'fa fa-times-circle fa-lg',
        validating: 'fa fa-refresh'
    }

    $('#form-normograma').bootstrapValidator({
            feedbackIcons: faIcon,
            excluded: ':disabled',
            fields: {
            norma: {
                validators: {
                    notEmpty: {
                        message: 'El nombre de la norma no puede ser vacío'
                    }
                }
            },
            palabras_clave: {
                validators: {
                    notEmpty: {
                        message: 'Las palabras clave de la norma no puede ser vacía'
                    }
                }
            },
            año: {
                validators: {
                    notEmpty: {
                        message: 'El año no puede ser vacía'
                    },
                    numeric: {
                        message: 'El año sólo puede contener números'
                    },
                }
            },
            sector: {
                validators: {
                    notEmpty: {
                        message: 'Debe seleccionar un sector'
                    }
                }
            },
            archivo: {
                validators: {
                    notEmpty: {
                        message: 'Debe subir un archivo adjunto al registro de la norma'
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