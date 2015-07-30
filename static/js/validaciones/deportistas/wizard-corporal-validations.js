form = "#form-wizard-corporal";
if(mujer == true){
    var min_grasa = 8;
    var max_grasa = 40;
}else{
    var min_grasa = 6;
    var max_grasa = 35;
}
fields = {
            peso: {
                validators: {
                    notEmpty: {
                        message: 'El peso del deportista no puede ser vacío'
                    },
                    numeric: {
                        message: 'El peso debe ser numérico'
                    },
                    greaterThan: {
                        message: 'El peso no puede ser menor o igual a 0',
                        value: 1

                    }

                }
            },
            estatura: {
                validators: {
                    notEmpty: {
                        message: 'La estatura del deportista no puede ser vacía'
                    },
                    numeric: {
                        message: 'La estatura debe ser numérica'
                    },
                    greaterThan: {
                        message: 'La estatura no puede ser menor o igual a 0',
                        value: 1

                    }
                }
            },
            RH: {
                validators: {
                    notEmpty: {
                        message: 'Por favor escoja un tipo de sangre'
                    }
                }
            },
            tipo_talla: {
                validators: {
                    notEmpty: {
                        message: 'Por favor escoja un tipo de talla'
                    }
                }
            },
            talla_camisa: {
                validators: {
                    notEmpty: {
                        message: 'Por favor escoja una talla de camisa'
                    }
                }
            },
            talla_pantaloneta: {
                validators: {
                    notEmpty: {
                        message: 'Por favor escoja una talla de pantaloneta'
                    }
                }
            },
            talla_zapato: {
                validators: {
                    notEmpty: {
                        message:'Por favor escoja una talla de zapato'
                    }
                }
            },
            imc: {
                validators: {
                    notEmpty: {
                        message:'Ingrese estatura y peso para calcular este valor'
                    },
                    greaterThan: {
                        message: 'Por favor ingrese datos reales para tener un calculo preciso',
                        value: 1

                    }
                }
            },
            porcentaje_grasa: {
                validators: {
                    notEmpty: {
                        message:'Este valor no puede ser vacío, ingreselo o presione calcular'
                    },
                    between : {
                        message: 'Por favor ingrese datos reales',
                        min: min_grasa,
                        max: max_grasa
                    }

                }
            },
            masa_corporal_magra: {
                validators: {
                    notEmpty: {
                        message: 'Ingrese o calcule el % de grasa corporal para poder calcular este dato'
                    },
                    greaterThan: {
                        message: 'Por favor ingrese datos reales para tener un calculo preciso',
                        value: 1

                    }
                }
            },
            eps: {
                validators: {
                    notEmpty: {
                        message:'Por favor seleccione una EPS, si no este en la lista seleccione Otra'
                    }
                }
            }


        };

$.getScript(base+"js/validaciones/validations-base.js");
