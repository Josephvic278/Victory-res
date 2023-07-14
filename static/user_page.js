
function file_f() {
    var file_input = document.getElementById("file");
    
    var file = file_input.files[0];
    var path = URL.createObjectURL(file);

    var file_name = file.name;
    var filen = document.getElementById("file_name")
    filen.value = file_name;

    var img = document.getElementById("dmi");
    img.src = path;
}

function open_addimage() {
    let add_image = document.getElementById("add_image")
    add_image.style.display = "block";
    add_image.style.display = "flex";
}
function close_add() {
    let add_image = document.getElementById("add_image")
    add_image.style.display = "none";
}
function  open_user_menu() {
    var user_menu = document.getElementById("user_menu")
    
    if (user_menu.style.display=="none") {
        user_menu.style.display="block"
        user_menu.style.display="flex"
    }else{
    
        user_menu.style.display="none"
        
    }
}

function  toggleLike(postId) {
    const button = document.querySelector(`button[data-post-id="${postId}"]`);
    
    const postImage = document.querySelector(`img[data-post-id="${postId}"]`)
    
    fp1 = document.getElementById("fp1").value;
    fp = document.getElementById("fp").value;
    
    const cr = window.location.href;
    var img_p = cr+"/"+"like1.png"
    let new_img_p = img_p.substring(0,img_p.length -18)
    let blue_img = new_img_p+"static/"+"like1.png"
    let gray_img = new_img_p+"static/"+"like.png"
    var uemail = document.getElementById("user_email").value
    
    if (postImage.src == gray_img) {
        postImage.src = fp;
        
        const socket = io();
        var data = [uemail,postId,"liked"]
        socket.emit('like-data',data);       
     }
    else {
        postImage.src = gray_img;
        const socket = io();
        var data = [uemail,postId,"unliked"]
        socket.emit('like-data',data);                           
    }  
}

function run_anim() {
  var element = document.getElementById("abtn");
  element.classList.toggle("ts")
}

function toggleOption(postid) {
    var opt_box_var = document.getElementById("opt_box");
    /*opt_box_var.style.display="block";*/
    
    const spec_opt = document.querySelector(`div[post-opt-id="${postid}"]`);
    spec_opt.style.display="block"
}

function close_opt_box(postid1) {
    const  close_opt = document.querySelector(`div[post-opt-id="${postid1}"]`);
    close_opt.style.display="none"
}

function delete_post(delete_post_id) {
    const socket = io();
    var data = {"delete":delete_post_id}
    socket.emit('delete-post',data)
}

function post_comment(comment_post_id) {
    const socket = io();
    var comment_value = document.querySelector(`textarea[comment-id="${comment_post_id}"]`)
    var ud = document.getElementById("ud").value
    if (comment_post_id.value != "" ) {
        data = [ud,comment_post_id,comment_value.value]
        socket.emit("comment",data)
    }
    comment_value.value = "";
    var c_alert = document.getElementById("c_alert")
    c_alert.style.visibility="visible"
    c_alert.style.transition="2s"
    c_alert.style.opacity="1"    
    c_alert.style.visibility="hidden"       
}

function comment_area(post_id) {    
    var post_com = document.querySelector(`div[post-id="${post_id}"]`)
    
    if (post_com == null) {
        document.getElementById("comment_area1").style.display="block"
    }
    else{
        post_com.style.display="block"
    }    
}

function close_comm(post_id1){
    var comm_ = document.querySelector(`div[post-id="${post_id1}"]`)
    comm_.style.display="none"
}