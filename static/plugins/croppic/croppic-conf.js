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
        },
        loadPicture:picture,
        onBeforeImgCrop:function(){},
        onAfterImgCrop: function(mns){

            var img = mns["url"];
            $("#imagen-hidden").val(img);

            console.log(mns);

            document.getElementById("clasificado-form").submit();

        },
        onError: function(err){console.log(err);}
    }

    cropperHeader = new Croppic('image-upload', cropperOptions);

    $(buttonReset).click(function(){
        cropperOptions["loadPicture"] = "";
        console.log("destroy");
        cropperHeader.destroy();
        cropperHeader = new Croppic('image-upload', cropperOptions);
    });


    $("#UploadImg").click(function(){
        if($('.cropControlUpload').is(':visible')){

            $("#modalTrigger2").removeClass("btn-danger").addClass("btn-default").html("Cargar Imagen");
            $("#labelImg").html("");
        }else{
            $("#modalTrigger2").removeClass("btn-default").addClass("btn-danger").html("Cambiar Imagen");
            $("#labelImg").html("Imagen lista para subir");
        }
    });
});





