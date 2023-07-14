document.addEventListener('DOMContentLoaded', function(){
    var def_v = 0
    var def = document.querySelector(`div[line_id="${def_v}"]`)
    def.style.borderBottom="5px solid #146C94" 
});

function tab_post(tab_id){
    var tab_post = document.getElementById("post_body");
    var tab_photos = document.getElementById("post_photos");
    if (tab_post.style.display!="block") {
       tab_post.style.display='block';
       tab_post.style.display="flex"
       tab_photos.style.display="none";
       for (id = 0;id < 4; id++) {
           var lines = document.querySelector(`div[line_id="${id}"]`)
          if (id!=tab_id) {
               lines.style.borderBottom="5px solid white"
               lines.style.width="0px"
           }
           else{
               lines.style.borderBottom="5px solid #146C94"
               lines.style.width="90px"
           } 
       }
    }
}
function tab_photos(tab_id){    
    var tab_photos = document.getElementById("post_photos");
    var tab_post = document.getElementById("post_body");
    if (tab_photos.style.display!="block") {
       tab_photos.style.display='block' 
       tab_photos.style.display="flex"
       tab_post.style.display="none"              
       for (id = 0;id < 4; id++) {
           var lines = document.querySelector(`div[line_id="${id}"]`)  
           if (id!=tab_id) {
               lines.style.borderBottom="5px solid white"
               lines.style.width="0px"               
           }
           else{
               lines.style.borderBottom="5px solid #146C94"
               lines.style.width="90px"
           }
       }     
    }
}
function add_f(btn_id,r_id) {
    var btn_add = document.getElementById("sug"+r_id)   
    btn_add.style.width="50%"
    btn_add.style.transition="0.7s"
    btn_add.textContent="Request Sent"
    const socket = io();
    data = {"request":[btn_id,r_id]}
    socket.emit('add_f',data)
}
function rem_f(btn_id) {
    alert(btn_id)
}
function accept_req(req_id) {
    var acc_btn = document.getElementById("acc"+req_id)
    acc_btn.style.width="100%"
    acc_btn.textContent=" Request Accepted"
    var dec_btn = document.getElementById("dec"+req_id)
    dec_btn.style.display="none"
    const socket = io();
    data = {"accepted":req_id}
    socket.emit("req_accept",data)       
}
function decline_req(req_id) {
    alert(req_id)
}
