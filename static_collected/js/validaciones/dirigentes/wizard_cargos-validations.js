form = "#form-wizard-cargos";
fields = {
    nombre: {
        validators: {
            notEmpty: {
                message: 'El cargo del dirigente no puede ser vacío'
            }
        }
    },
    fecha_posesion: {
        validators: {
            notEmpty: {
                message: 'La fecha de posesión del dirigente no puede ser vacía'
            },
            date: {
                message: 'El valor ingresado no es una fecha válida',
                format: 'YYYY-MM-DD',
                max: 'fecha_retiro'
            }
        }
    },
    fecha_retiro: {
        validators: {
            date: {
                message: 'El valor ingresado no es una fecha válida',
                format: 'YYYY-MM-DD',
                min: 'fecha_posesion'
            }
        }
    },
    vigencia_inicio: {
        validators: {
            notEmpty: {
                message: 'La fecha de inicio de vigencia del periodo no puede ser vacía'
            },
            date: {
                message: 'El valor ingresado no es una fecha válida',
                format: 'YYYY-MM-DD',
                max: 'vigencia_fin'
            }
        }
    },
    vigencia_fin: {
        validators: {
            notEmpty: {
                message: 'La fecha de fin de vigencia del periodo no puede ser vacía'
            },
            date: {
                message: 'El valor ingresado no es una fecha válida',
                format: 'YYYY-MM-DD',
                min: 'vigencia_inicio'
            }
        }
    },
};
//Revalidar campos al ser actualizados
$("#id_fecha_posesion").on('change',function(e){
    $("#form-wizard-cargos").bootstrapValidator('revalidateField', 'fecha_posesion');
});
$("#id_fecha_retiro").on('change',function(e){
    $("#form-wizard-cargos").bootstrapValidator('revalidateField', 'fecha_retiro');
});
$("#id_vigencia_inicio").on('change',function(e){
    $("#form-wizard-cargos").bootstrapValidator('revalidateField', 'vigencia_inicio');
});
$("#id_vigencia_fin").on('change',function(e){
    $("#form-wizard-cargos").bootstrapValidator('revalidateField', 'vigencia_fin');
});
$.getScript(base+"js/validaciones/validations-base.js");