/**
 * Created by juandgc on 12/04/16.
 */

$(btnForm).click(function(e){
    console.log("antes validate");
    $("#"+ loadForm).bootstrapValidator('validate');
    if ($("div.form-group").hasClass("has-error")) {
        console.log("dentro if");
        e.preventDefault();
        return false;
    }
    $(".q-hide").removeClass("hide");
    $("div.q-hide").css({"opacity":"0.8", "z-index": "2000"});
    console.log("dentro else");
    document.getElementById(loadForm).submit();
});