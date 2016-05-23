/**
 * Created by daniel on 18/05/16.
 */
$("#id_internacional").on('change',function(){
    var check = $(this).is(":checked");
    if(check){
        $("#id_nombre").attr('type','text');
        $("#id_nombre").prop('required',true);
        $("#entidades").css('display','none');
        $("#id_entidad").prop('required',false);

    }else{
        $("#id_nombre").attr('type','hidden');
        $("#id_nombre").prop('required',false);
        $("#entidades").css('display','block');
        $("#id_entidad").prop('required',true);
    }
})