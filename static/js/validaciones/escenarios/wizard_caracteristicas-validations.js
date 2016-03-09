$(document).ready(function() {
    //Revalidar campos que usan plugins al ser actualizados
    

    var faIcon = {
        valid: 'fa fa-check-circle fa-lg text-success',
        invalid: 'fa fa-times-circle fa-lg',
        validating: 'fa fa-refresh'
    };

    $('#form-wizard-escenarios').bootstrapValidator({
            feedbackIcons: faIcon,
            excluded: ':disabled',
            fields: {
                plano_archivo: {
                    validators: {
                        file: {
                            extension: 'pdf',
                            type: 'application/pdf',
                            maxSize: 3170304,   // 2048 * 1024
                            message: 'Por favor escoja un archivo en formato pdf menor a 3MB'
                        }
                    }
                },
                ficha_catastral: {
                    validators: {
                        file: {
                            extension: 'pdf',
                            type: 'application/pdf',
                            maxSize: 3170304,   // 2048 * 1024
                            message: 'Por favor escoja un archivo en formato pdf menor a 3MB'
                        }
                    }
                },
                certificado_tradicio_libertad: {
                    validators: {
                        file: {
                            extension: 'pdf',
                            type: 'application/pdf',
                            maxSize: 3170304,   // 2048 * 1024
                            message: 'Por favor escoja un archivo en formato pdf menor a 3MB'
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