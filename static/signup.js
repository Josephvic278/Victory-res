function check_pass() {
    pass_input = document.getElementById("password").value;
    first_err = document.getElementById("fp");
    second_err = document.getElementById("fp2")
    third_err = document.getElementById("fp3")
    sb_c = document.getElementById("sub");
        
    if (pass_input.length > 8) {
        first_err.style.background = "green";
    } else {
        first_err.style.background = "red";
    }

    var simlist = /[._%|=<>{}@#£_&-+()*""'':;!?]/;
    if (simlist.test(pass_input)){
        second_err.style.background = "green";
        sb_c.disabled=false;
    }
    else{
        second_err.style.background = "red";
        sb_c.disabled=true;
    }
     
    if (pass_input !== pass_input.toLowerCase()) {
        third_err.style.background = "green";
        } 
    else {
            third_err.style.background = "red";
        }
    }

    function eye() {
        pass_i = document.getElementById("password");
        if (pass_i.type == "password") {
            pass_i.type = "text"
        } else {
            pass_i.type = "password"
        }

    }

    function in_c() {
        sb_c = document.getElementById("sub");
        sb_c.disabled = false;
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
                data_list[i].style.border = "2px solid red"
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
