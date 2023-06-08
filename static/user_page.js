
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
        alert(data)
        socket.emit('like-data',data);
        
        socket.on('response', function(response) {
            alert(response.message);
        });    
     }
    else {
        postImage.src = gray_img;
        const socket = io();
        var data = [uemail,postId,"unliked"]
        alert(data)
        socket.emit('like-data',data);
        
        socket.on('response', function(response) {
            alert(response.message);
        });    
        
    }  
}
