function check_pass() {
  const pass_input = document.getElementById("password").value;
  const pass_track = document.getElementById("pass_track");
  const sb_c = document.getElementById("sub");

  const simlist = /[._%|=<>{}@#£_&-+()*""'':;!?,$]/;
  const pass_len = pass_input.length > 8;
  const pass_upper = /[A-Z]/.test(pass_input);
  const pass_sym = simlist.test(pass_input);
  let pass_text = document.getElementById("pass_text")

  let strength = 0;

  if (pass_len) {
    strength += 25;
    pass_track.style.backgroundColor = "red";
    pass_track.style.width = strength + "%";
    pass_text.textContent = "Ok"
  } else {
    pass_track.style.width = "0%";
    pass_text.textContent = "Not good enough"
  }

  if (pass_sym) {
    strength += 25;
    pass_track.style.backgroundColor = "yellow";
    pass_track.style.width = strength + "%";
    sb_c.disabled = false;
    pass_text.textContent = "Good"
  } else {
    pass_track.style.width = strength + "%";
    pass_track.style.backgroundColor = "red";
    sb_c.disabled = true;
    pass_text.textContent = "Need a little work"
  }

  if (pass_upper) {
    strength += 25;
    pass_track.style.backgroundColor = "green";
    pass_track.style.width = strength + "%";
    pass_text.textContent = "Excellent"
  } else {
    pass_track.style.width = strength + "%";
  }
}

    function run() {
        fn = document.getElementById("firstname");
        ln = document.getElementById("lastname");
        un = document.getElementById("username");
        em = document.getElementById("email");
        ps = document.getElementById("password");
        sb = document.getElementById("sub");

        let comf = ""
        const data_list = [fn,
            ln,
            un,
            em,
            ps]
        for (i = 0; i < data_list.length; i++) {
            if (data_list[i].value == "") {
                data_list[i].style.boxShadow = "0 5px 5px rgba(255, 0, 0, 0.1)"
            } else {
                comf = comf+"t"
            }
        }

        if (comf.length == 5) {
            sb.disabled = false;
        } else {
            sb.disabled = true;

        }
        
        setInterval(in_c, 2000)
    }

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
