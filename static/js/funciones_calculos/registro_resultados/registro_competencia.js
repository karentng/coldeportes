$(document).ready(function() {
    $("#id_categoria").prop("disabled", true);
    $("#id_modalidad").prop("disabled", true);
});
$("#id_disciplina_deportiva").on('change',function(){
    var val_depor = $(this).val();
    ajax_modalidades(val_depor);
    ajax_categorias(val_depor);
});
function ajax_modalidades(depor){
    $("#id_modalidad").empty();
    $.ajax({
        url: '/deportistas/modalidades/get/'+depor,
        dataType: 'json',
        success: function(response) {
            $("#id_modalidad").prop("disabled", false);
            var datos = response.data;
            $("#id_modalidad").select2({
              data: datos
            })
        },
        error: function(err){
            $("#id_modalidad").prop("disabled", true);
            $("#id_modalidad").select2({
              data: null
            });
            $("#id_modalidad").empty();
            console.log(err)
        }
    });
}
function ajax_categorias(depor){
    $("#id_categoria").empty();
    $.ajax({
        url: '/deportistas/categorias/get/'+depor,
        dataType: 'json',
        success: function(response) {
            $("#id_categoria").prop("disabled", false);
            var datos = response.data;
            $("#id_categoria").select2({
                data:datos
            });
        },
        error: function(err){
            $("#id_categoria").prop("disabled", true);
            $("#id_categoria").select2({
                data:null
            });
            $("#id_categoria").empty();
            console.log(err)
        }
    });
}