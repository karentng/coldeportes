form = "#form-wizard-funciones";
fields = {
    descripcion: {
        validators: {
            notEmpty: {
                message: 'La descripción de la función para el cargo no puede ser vacía'
            }
        }
    },
    cargo: {
        validators: {
            notEmpty: {
                message: 'Debe de seleccionar un cargo para agregarle funciones'
            },
        }
    }
};
$.getScript(base+"js/validaciones/validations-base.js");