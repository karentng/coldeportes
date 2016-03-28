/**
 * Created by diegoamt on 28/03/16.
 */

form = "#form-wizard-mantenimiento";
fields = {
    fecha_ultimo_mantenimiento: {
        validators: {
            notEmpty: {
                message: "La fecha del mantenimiento no puede ser vacía"
            },
            date: {
                format: "YYYY-MM-DD",
                message: "La fecha no es válida"
            }
        }
    },
    descripcion_ultimo_mantenimiento: {
        validators: {
            notEmpty: {
                message: "La descripción del mantenimiento no puede ser vacía"
            }
        }
    },
    periodicidad: {
        validators: {
            notEmpty: {
                message: "La periodicidad del mantenimiento no puede ser vacía"
            }
        }
    },
};
$("#id_fecha_ultimo_mantenimiento").on('change',function(e){
   $(form).bootstrapValidator('revalidateField', 'fecha_ultimo_mantenimiento');
});
$.getScript(base+"js/validaciones/validations-base.js");