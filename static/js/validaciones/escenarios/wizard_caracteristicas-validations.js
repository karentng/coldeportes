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
                            extension: 'pdf,rar,zip,jpeg,jpg,png',
                            type: 'application/pdf,application/x-rar-compressed,application/zip,image/jpeg,image/png',
                            maxSize: 5242880,   // 5120 * 1024
                            message: 'Por favor escoja un archivo en formato pdf, rar, zip, jpeg, jpg o png menor a 5MB'
                        }
                    }
                },
                ficha_catastral: {
                    validators: {
                        file: {
                            extension: 'pdf,rar,zip,jpeg,jpg,png',
                            type: 'application/pdf,application/x-rar-compressed,application/zip,image/jpeg,image/png',
                            maxSize: 5242880,   // 5120 * 1024
                            message: 'Por favor escoja un archivo en formato pdf, rar, zip, jpeg, jpg o png menor a 5MB'
                        }
                    }
                },
                certificado_tradicio_libertad: {
                    validators: {
                        file: {
                            extension: 'pdf,rar,zip,jpeg,jpg,png',
                            type: 'application/pdf,application/x-rar-compressed,application/zip,image/jpeg,image/png',
                            maxSize: 5242880,   // 5120 * 1024
                            message: 'Por favor escoja un archivo en formato pdf, rar, zip, jpeg, jpg o png menor a 5MB'
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