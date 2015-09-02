form = "#form-wizard-academica";
fields = {
            pais: {
                validators: {
                    notEmpty: {
                        message: 'Por favor escoja un país'
                    }
                }
            },
            institucion: {
                validators: {
                    notEmpty: {
                        message: 'La institución de formación no puede ser vacía'
                    }
                }
            },
            nivel: {
                validators: {
                    notEmpty: {
                        message: 'Por favor escoja un nivel'
                    }
                }
            },
            estado: {
                validators: {
                    notEmpty: {
                        message: 'Por favor escoja un estado'
                    },
                }
            },
            grado_semestre: {
                validators: {
                    numeric: {
                        message: 'El grado, año o semestre debe ser un numero'
                    },
                }
            },
            fecha_finalizacion: {
                validators: {
                    numeric: {
                        message: 'El año de finalización debe ser un numero'
                    },
                }
            }

        };
$.getScript(base+"js/validaciones/validations-base.js");
