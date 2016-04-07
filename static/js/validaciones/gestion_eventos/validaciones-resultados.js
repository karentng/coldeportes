form = "#form-resultado";
fields = {
    reconocimiento: {
        validators: {
            notEmpty: {
                message: "El nombre del reconociemiento no puede servacío"
            }
        }
    },
    paticipante_reconocido: {
        validators: {
            notEmpty: {
                message: 'El campo del participante no puede ser vacío'
            }
        }
    }
};

$.getScript(base+"js/validaciones/validations-base.js");
