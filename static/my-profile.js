var tab_doc = document.getElementById("tab");
var tab_v = tab_value.value

function tab_photos() {
    if (tab_v != "photos") {
        document.getElementById("post_body").style.display="none"
        tab_v = "photos";
        
        var new_photo_s = document.getElementById("post_photos").style.display="flex"
        new_photo_s.style.display="block"
    }
}
