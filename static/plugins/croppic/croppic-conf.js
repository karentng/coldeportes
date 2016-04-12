/**
 * Created by juandgc on 11/02/16.
 */

$(document).ready(function(){
    var cropperHeader;
    var cropperOptions = {
        imgEyecandy:true,
        imgEyecandyOpacity:0.2,
        processInline:true,
        cropUrl:urlCrop,
        cropData:{
            "url_media": urlMedia
        },
        loadPicture:picture == "" || picture == "/media/" ? null : picture,
        onBeforeImgCrop:function(){},
        onAfterImgCrop: function(mns){

            var img = mns["url"];
            var status = mns["status"];
            if(status != "error"){
                $("#imagen-hidden").val(img);
            }
            console.log(mns);
            document.getElementById(formId).submit();

        },
        onError: function(err){console.log(err);}
    };

    cropperHeader = new Croppic('image-upload', cropperOptions);

    $("#reset-crop").click(function(){
        cropperOptions["loadPicture"] = "";
        console.log("destroy");
        cropperHeader.destroy();
        cropperHeader = new Croppic('image-upload', cropperOptions);
    });

    $('#submit-crop').click(function(event){
        event.preventDefault();
        if (edicion) {
            if ($("#modalTrigger2").hasClass("btn-info") && $('.cropControls.cropControlsCrop').length) {
                $("#imagen-hidden").val("si");
                document.getElementById(formId).submit();
                return false;
            } else {
                $("#" + formId).bootstrapValidator('validate');
                if ($("div.form-group").hasClass("has-error")) {
                    return false;
                } else {
                    if ($('.cropControls.cropControlsCrop').length) {
                        console.log("Cortando");
                        $('.cropControlCrop').click();
                    } else {
                        document.getElementById(formId).submit();
                        return false;
                    }
                }
            }
        }else{

            $("#"+formId).bootstrapValidator('validate');

            if($("div.form-group").hasClass("has-error")){
                return false;
            }else {
                if($('.cropControls.cropControlsCrop').length) {
                    console.log("Cortando");
                    $('.cropControlCrop').click();
                }else{
                    document.getElementById(formId).submit();
                    return false;
                }
            }
        }
    });

    $(window).keydown(function(event){
        if(event.keyCode == 13 || event.which == 13) {
            event.preventDefault();
            return false;
        }
    });
    $(document).on('ready',".add-tooltip",function(){
        $(this).tooltip();
    });
    $("#myModalCrop").bind('hidden.bs.modal',function(){
        if(!$('.cropControls.cropControlsCrop').length){

            $("#modalTrigger2").removeClass("btn-success").addClass("btn-primary").html("Cargar Imagen");
            $("#labelImg").html("No se ha seleccionado una imagen");
        }else{

            $("#modalTrigger2").removeClass("btn-primary").addClass("btn-success").html("Cambiar Imagen");
            $("#labelImg").html("Imagen lista para subir");
        }
    });
});





