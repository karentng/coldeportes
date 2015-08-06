/**
 * Created by daniel on 29/07/15.
 */
$('#id_peso').change(function() {
    var altura = $('#id_estatura').val() / 100;
    if (altura != undefined){
        var peso = $(this).val();
        var imc  =  (peso/(altura*altura)).toFixed(2);
        $('#id_imc').val(imc);
        $(form).bootstrapValidator('revalidateField', 'imc');
    }
});

$('#id_estatura').change(function() {
    var peso = $('#id_peso').val();
    if (peso != undefined){
        var altura = $(this).val() / 100;
        var imc  =  (peso/(altura*altura)).toFixed(2);
        $('#id_imc').val(imc);
        $(form).bootstrapValidator('revalidateField', 'imc');
    }
});
function masa_magra() {
    var peso = $('#id_peso').val();
    var magra = (peso*((100 - $('#id_porcentaje_grasa').val()) / 100)).toFixed(2);
    $('#id_masa_corporal_magra').val(magra);
    $(form).bootstrapValidator('revalidateField', 'masa_corporal_magra');
};

$('#id_porcentaje_grasa').change(function () {
    var peso = $('#id_peso').val();
    var magra = (peso*((100 - $('#id_porcentaje_grasa').val()) / 100)).toFixed(2);
    $('#id_masa_corporal_magra').val(magra);
    $(form).bootstrapValidator('revalidateField', 'masa_corporal_magra');
});

function calculo_cuello() {
    var cintura = $('#id_cintura').val();
    var altura = $('#id_estatura').val();
    var cuello = $('#id_cuello').val();
    if (mujer == true){
        var cadera = $('#id_cadera').val()/100;
        if(cintura != undefined && cadera!=undefined){
            var grasa = ((495 / (1.29579- 0.35004 * (Math.log10(cintura+cadera - cuello))  +0.22100*(Math.log10(altura))) )-450).toFixed(2);
            $('#id_porcentaje_grasa').val(grasa);
            masa_magra();
             $(form).bootstrapValidator('revalidateField', 'porcentaje_grasa');
        }
    }else{
        if(cintura != undefined){
            var grasa = ((495/ (1.0324 - (0.19077 * (Math.log10( cintura - cuello ))) + (0.15456 * (Math.log10(altura)) ) ) ) - 450).toFixed(2);
            $('#id_porcentaje_grasa').val(grasa);
            masa_magra();
             $(form).bootstrapValidator('revalidateField', 'porcentaje_grasa');
        }
    }

};

function calculo_cintura() {
    var cuello = $('#id_cuello').val();
    var altura = $('#id_estatura').val();
    var cintura = $('#id_cintura').val();
    if (mujer){
        var cadera = $('#id_cadera').val();
        if(cuello != undefined && cadera!=undefined){
            var grasa = ((495/(1.29579-0.35004*(Math.log10(cintura+cadera-cuello))+0.22100*(Math.log10(altura))))-450).toFixed(2);
            $('#id_porcentaje_grasa').val(grasa);
            masa_magra();
            $(form).bootstrapValidator('revalidateField', 'porcentaje_grasa');
        }
    }else{
        if(cuello != undefined){
            var grasa = ((495/(1.0324-0.19077*(Math.log10(cintura-cuello))+0.15456*(Math.log10(altura))) ) -450).toFixed(2);
            $('#id_porcentaje_grasa').val(grasa);
            masa_magra();
            $(form).bootstrapValidator('revalidateField', 'porcentaje_grasa');
        }
    }

};
function calculo_cadera() {
    var cintura = $('#id_cintura').val();
    var altura = $('#id_estatura').val();
    var cuello = $('#id_cuello').val();
    if(cintura != undefined && altura !=undefined && cuello!=undefined){
        var grasa = ((495/(1.29579-0.35004*(Math.log10(cintura+$('#id_cadera').val()-cuello))+0.22100*(Math.log10(altura))))-450).toFixed(2);
        $('#id_porcentaje_grasa').val(grasa);
        masa_magra();
        $(form).bootstrapValidator('revalidateField', 'porcentaje_grasa');
    }
};
