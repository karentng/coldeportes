/**
 * Created by Yalile Bermudes on 4/03/16.
 * Valiodacion de los campos de resgistro y edicion de los planes de costo
 */

form = "#plan-de-costo-form";

fields = {
    nombre: {
        validators:{
            notEmpty: {
                message: "El nombre del plan de costo no puede ser vacío"
            },
            stringLength: {
                message: 'El nombre del plan debe tener menos de 200 caracteres',
                max: function (value, validator, $field) {
                    return 200 - (value.match(/\r/g) || []).length;
                }
            }
        }
    },

    precio: {
        validators:{
            notEmpty: {
                message: "El precio del plan de costo no puede ser vacío"
            },
            integer: {
                message: 'El precio debe ser un número entero'
            },
            greaterThan: {
                value: 0,
                message: 'El precio debe ser mayor que o igual a 0'
            }
        }
    },

    descripcion: {
        validators:{
            notEmpty: {
                message: "La descripción del plan de costo no puede ser vacío"
            },
            stringLength: {
                message: 'la descripción del plan debe tener menos de 600 caracteres',
                max: function (value, validator, $field) {
                    return 200 - (value.match(/\r/g) || []).length;
                }
            }
        }
    }
};

$.getScript(base+"js/validaciones/validations-base.js");