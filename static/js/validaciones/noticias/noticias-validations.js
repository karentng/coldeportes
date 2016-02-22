form = "#form-noticia";
fields = {
    titulo: {
        validators: {
            notEmpty: {
                message: "El título de la noticia no puede ser vacío"
            }
        }
    },
    cuerpo_noticia: {
        validators: {
            notEmpty: {
                message: "El cuerpo de la noticia no puede ser vacío"
            }
        }
    },
    fecha_inicio: {
        validators: {
            notEmpty: {
                message: 'La fecha de inicio de la noticia no puede ser vacía'
            },
            date: {
                message: 'El valor ingresado no es una fecha válida',
                format: 'YYYY-MM-DD',
                max: 'fecha_expiracion'
            }
        }
    },
    fecha_expiracion: {
        validators: {
            notEmpty: {
                message: 'La fecha de finalización de la noticia no puede ser vacía'
            },
            date: {
                message: 'El valor ingresado no es una fecha válida',
                format: 'YYYY-MM-DD',
                min: 'fecha_inicio'
            }
        }
    }
};



//Revalidar campos al ser actualizados
$("#id_fecha_inicio").on('change',function(e){
    $("#form-noticia").bootstrapValidator('revalidateField', 'fecha_inicio');
});
$("#id_fecha_expiracion").on('change',function(e){
    $("#form-noticia").bootstrapValidator('revalidateField', 'fecha_expiracion');
});

$.getScript(base+"js/validaciones/validations-base.js");


$(document).ready(function(){
    $("#id_cuerpo_noticia")
        .ckeditor({
            language: 'es',
            uiColor: '#008A8A'
        })
            .editor
                // To use the 'change' event, use CKEditor 4.2 or later
                .on('change', function() {
                    // Revalidate the bio field
                    $('#form-noticia').bootstrapValidator('revalidateField', 'cuerpo_noticia');
                });
});