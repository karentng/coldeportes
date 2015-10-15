$('#id_superior').change(function(){
    var id = $(this).val();

    $.ajax({
        url : '/dirigentes/cargos',
        type: 'GET',
        dataType: 'json',
        data: {'dirigente_id': id},
        success: function(data){
            var select = clear_superior_cargo();
            var cargos = data['cargos'];
            for(var i=0;i<cargos.length;i++){
                var cargo = cargos[i];
                select.append($("<option />").val(cargo.value).text(cargo.text));
            }
        },
        error: function(){
            clear_superior_cargo();//puede dar error cuando se selecciona el superior vacio
        }
    });
});

function clear_superior_cargo(){
    var superior_cargo = $('#id_superior_cargo');
    superior_cargo.empty().append($("<option />").val('').text('--------').attr('selected','selected'));
    return superior_cargo;
}

clear_superior_cargo();//se limpia el campo, al iniciar contiene todos los posibles cargos