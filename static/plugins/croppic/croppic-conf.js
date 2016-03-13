/**
 * Created by juandgc on 11/02/16.
 */

$(document).ready(function(){
    var cropperHeader;

    var cropperOptions = {
        imgEyecandy:true,
        imgEyecandyOpacity:0.2,
        processInline:true,
        uploadUrl:'{}',
        uploadData:{
            "csrfmiddlewaretoken":csrftoken,
        },
        cropUrl:urlCrop,
        cropData:{
            "csrfmiddlewaretoken":csrftoken,
            "url_media": urlMedia
        },
        loadPicture:picture,
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

    $(buttonReset).click(function(){
        cropperOptions["loadPicture"] = "";
        console.log("destroy");
        cropperHeader.destroy();
        cropperHeader = new Croppic('image-upload', cropperOptions);
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
            $("#labelImg").html("");
        }else{

            $("#modalTrigger2").removeClass("btn-primary").addClass("btn-success").html("Cambiar Imagen");
            $("#labelImg").html("Imagen lista para subir");
        }
    });
});





