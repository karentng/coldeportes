form = '#form-formacion';
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
                    greaterThan: {
                        message: 'El grado,año o semestre no puede ser menor o igual a 0',
                        value: 1

                    }
                }
            },
            fecha_finalizacion: {
                validators: {
                    numeric: {
                        message: 'El año de finalización debe ser un numero'
                    },
                    greaterThan: {
                        message: 'El año de finalización no puede ser menor o igual a 1950',
                        value: 1950

                    }
                }
            }

        };
$.getScript(base+"js/validaciones/validations-base.js");