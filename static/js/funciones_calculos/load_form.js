/**
 * Created by juandgc on 12/04/16.
 */

$(loadForm).submit(function(e){
    $(".q-hide").removeClass("hide");
    $("div.q-hide").css({"opacity":"0.8", "z-index": "2000"});
});