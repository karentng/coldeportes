form = "#form-verificacion";
fields= {
    identificacion: {
        validators: {
            notEmpty: {
                message: 'El número de identificación no puede ser vacío'
            },
            regexp: {
                regexp: "^[0-9a-zA-Z]+$",
                message: 'El número de identificación solo puede contener números ó letras'
            }
        }
    },
};

$.getScript(base+"js/validaciones/validations-base.js");