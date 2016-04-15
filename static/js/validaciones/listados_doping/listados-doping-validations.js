form = "#form-caso-doping";
fields = {
    identificacion: {
        validators: {
            notEmpty: {
                message: "Este campo no puede ser vacío"
            },
            numeric: {
                message: "Este campo solo puede contener números"
            }
        }
    },
    nombres_sancionado: {
        validators: {
            notEmpty: {
                message: "Este campo no puede ser vacío"
            }
        }
    },
    apellidos_sancionado: {
        validators: {
            notEmpty: {
                message: 'Este campo no puede ser vacío'
            }
        }
    },
    tipo_sancion: {
        validators: {
            notEmpty: {
                message: 'Este campo no puede ser vacío'
            }
        }
    },
    duracion_sancion: {
        validators: {
            notEmpty: {
                message: 'Este campo no puede ser vacío'
            }
        }
    }
};

$("#id_nombres_sancionado").change(function(e){
    console.log("cambió");
    $("#form-caso-doping").bootstrapValidator('revalidateField', 'nombres_sancionado');
});

$("#id_apellidos_sancionado").change(function(e){
    console.log("cambió");
    $("#form-caso-doping").bootstrapValidator('revalidateField', 'apellidos_sancionado');
});

$.getScript(base+"js/validaciones/validations-base.js");


