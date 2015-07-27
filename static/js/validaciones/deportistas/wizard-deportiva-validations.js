form = "#form-wizard-deportiva";
fields = {
            nombre: {
                validators: {
                    notEmpty: {
                        message: 'El nombre del campeonato no puede ser vació'
                    }
                }
            },
            pais: {
                validators: {
                    notEmpty: {
                        message: 'Por favor escoja un país'
                    }
                }
            },
            institucion_equipo: {
                validators: {
                    notEmpty: {
                        message: 'El Club Deportivo no puede ser vació'
                    }
                }
            },
            tipo: {
                validators: {
                    notEmpty: {
                        message: 'Por favor escoja un tipo de campeonato'
                    }
                }
            },
            puesto: {
                validators: {
                    notEmpty: {
                        message: 'El puesto no puede ser vació'
                    },
                    numeric: {
                        message: 'El puesto debe ser numérico'
                    },
                }
            },
            categoria: {
                validators: {
                    notEmpty: {
                        message: 'La categoría no puede ser vaciá'
                    },
                }
            }

        };
$.getScript(base+"js/validaciones/validations-base.js");
