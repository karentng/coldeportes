form = "#form-adjunto-solicitud";
fields = {
            archivo: {
                validators: {
                    notEmpty: {
                        message: 'Debe seleccionar un archvio para poder adicionarlo'
                    }
                }
            }
        };
$.getScript(base+"js/validaciones/validations-base.js");
