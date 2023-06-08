function passcheck(){
     var pass_img = document.getElementById("pass_img")
     var pass_bar = document.getElementById("password")
     
     if (pass_img.src == 'http://localhost:5000/static/closedeye.png') {
         pass_img.src = 'http://localhost:5000/static/openeye.png';
         pass_bar.type = "text";
     }
     
     else{
         pass_img.src = 'http://localhost:5000/static/closedeye.png';
         pass_bar.type = "password";
     }
}
