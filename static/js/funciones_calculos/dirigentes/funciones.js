var modal = "<div class='modal fade' id='modal-desactivate{funcion_id}'> <div class='modal-dialog'> <div class='modal-content'> <div class='modal-header'> <button type='button' class='close' data-dismiss='modal' aria-hidden='true'>×</button> <h4 class='modal-title'>Eliminar Función:</h4> </div> <div class='modal-body'> ¿Está seguro que desea eliminar esta función? </div> <div class='modal-footer'> <a href='javascript:;' class='btn btn-sm btn-white' data-dismiss='modal'>Cancelar</a> <a href='/dirigentes/eliminar/funcion/{dirigente_id}/{cargo_id}/{funcion_id}' class='btn btn-sm btn-warning'>Aceptar</a> </div> </div> </div> </div>"
var link_modal = "<a href='#modal-desactivate{funcion_id}' data-toggle='modal'><i class='fa fa-trash'></i></a>"

function clear_funciones(){
    var tabla = $('table tbody');
    tabla.empty();
    return tabla;
}

function get_funciones(value){
    var id_cargo = value;
    var id_dirigente = $('#id_dirigente').val();

    $.ajax({
        url : '/dirigentes/funciones',
        type: 'GET',
        dataType: 'json',
        data: {'id_cargo': id_cargo, 'id_dirigente': id_dirigente},
        success: function(data){
            var funciones = data['funciones'];
            var tabla = clear_funciones();

            for(var i=0;i<funciones.length;i++){
                var funcion = funciones[i];
                var lm = link_modal.replace('{funcion_id}',funcion.id);
                var m = modal.replace(/{funcion.id}/g,funcion.id).replace('{dirigente_id}',id_dirigente).replace('{cargo_id}',id_cargo);
                var fila = "<tr><td align='center'>"+funcion.descripcion+"</td>";
                fila += "<td align='center'>" + lm + m + "</td></tr>";
                tabla.append(fila);
            }
        },
        error: function(){
            clear_funciones();
        }
    });
}

var cargo = $('#id_cargo');
//si el select cambia se actualizan las funciones
cargo.change(function(){
    get_funciones(cargo.val());
});
//si el select tiene un valor inicial cuando la página carga se actualizan sus funciones
//(por ejemplo, después de grabar una funcion nueva o de eliminar una existente)
get_funciones(cargo.val());