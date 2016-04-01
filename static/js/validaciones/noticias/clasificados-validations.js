form = "#clasificado-form";
var init_date;
fields = {
    titulo: {
        validators: {
            notEmpty: {
                message: "El título del clasificado no puede ser vacío"
            }
        }
    },
    descripcion: {
        validators: {
            notEmpty: {
                message: "La descripción del clasificado no puede ser vacío"
            }
        }
    },
    contacto: {
        validators: {
            notEmpty: {
                message: "El contacto del clasificado no puede ser vacío"
            }
        }
    },
    fecha_publicacion: {
        validators: {
            notEmpty: {
                message: 'La fecha de publicación del clasificado no puede ser vacía'
            },
            date: {
                message: 'El valor ingresado debe ser mayor o igual que hoy y menor que la fecha de expiración',
                format: 'YYYY-MM-DD',
                max: 'fecha_expiracion',
                min: function(field, validator){
                    console.log(init_date);
                    if(init_date != ""){
                        return "2016-01-01";
                    }
                    var d = new Date();

                    var curr_date = d.getDate();

                    var curr_month = d.getMonth() + 1;

                    var curr_year = d.getFullYear();
                    return curr_year + "-" + curr_month + "-" + curr_date;

                }
            }
        }
    },
    fecha_expiracion: {
        validators: {
            notEmpty: {
                message: 'La fecha de expiración del clasificado no puede ser vacía'
            },
            date: {
                message: 'La fecha de expiración debe ser mayor a la de inicio',
                format: 'YYYY-MM-DD',
                min: 'fecha_publicacion'
            }
        }
    }
};


var form = $("#clasificado-form");

//Revalidar campos al ser actualizados
$("#id_fecha_publicacion").on('change',function(e){
    form.bootstrapValidator('revalidateField', 'fecha_expiracion');
    form.bootstrapValidator('revalidateField', 'fecha_publicacion');

});

$("#id_fecha_expiracion").on('change',function(e){
    form.bootstrapValidator('revalidateField', 'fecha_expiracion');
    form.bootstrapValidator('revalidateField', 'fecha_publicacion');
});

$.getScript(base+"js/validaciones/validations-base.js");

$(document).ready(function(){
    init_date = $("input#id_fecha_publicacion").val();

});