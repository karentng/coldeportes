form = "#form-resultado";
fields = {
    cantidad_puestos: {
        validators: {
            notEmpty: {
                message: "La cantidad de puestos no puede ser vacía"
            }
        }
    },
    primer_lugar: {
        validators: {
            notEmpty: {
                message: 'El campo primer lugar no puede ser vacío'
            }
        }
    },
    segundo_lugar: {
        validators: {
            callback: {
                message: 'El campo segundo lugar no puede ser vacío',
                callback: function(value, validator){
                    var cantidadPuestos = $("#id_cantidad_puestos").find("option:selected").val();
                    console.log(value);
                    if(cantidadPuestos > 1) {
                        return value != "";
                    }
                    return true;
                }
            }
        }
    },
    tercer_lugar: {
        validators: {
            callback: {
                message: 'El campo tercer lugar no puede ser vacío',
                callback: function(value, validator){
                    console.log(value);
                    var cantidadPuestos = $("#id_cantidad_puestos").find("option:selected").val();
                    return !(cantidadPuestos > 2) && value != null;
                }
            }
        }
    }
};

$.getScript(base+"js/validaciones/validations-base.js");
