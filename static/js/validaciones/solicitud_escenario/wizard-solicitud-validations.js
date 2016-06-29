form = "#form-solicitud-escenario";
fields = {
            prioridad: {
                validators: {
                    notEmpty: {
                        message: 'Debe escoger una prioridad'
                    }
                }
            },
            escenarios: {
                validators: {
                    notEmpty: {
                        message: 'Debe escoger al menos 1 escenario'
                    }
                }
            },
            para_quien: {
                validators: {
                    notEmpty: {
                        message: 'Debe especificar para que ente va dirigida la solicitud'
                    }
                }
            },
            descripcion: {
                validators: {
                    notEmpty: {
                        message: 'Debe describir la solicitud'
                    },
                    stringLength: {
                        message: 'El tamaño de la descripción debe tener como maximo 500 caracteres',
                        max: 500
                    }

                }
            }
        };
$.getScript(base+"js/validaciones/validations-base.js");
