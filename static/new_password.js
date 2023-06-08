function check_input() {
    input_bar = document.getElementById("input")
    sub_btn = document.getElementById("btn")
    msg = document.getElementById("msg")
    input_bar1 = document.getElementById("input2")
    
    if (input_bar.value == "") {
        sub_btn.disabled = true;
    }
    else{
        sub_btn.disabled = false;
    }
    
    if (input_bar.value == input_bar1.value) {
        sub_btn.disabled = false
    }
    else{
        msg.textContent="Passwords does not match"
        sub_btn.disabled = true
    }
}

function type_checker() {
    input_bar = document.getElementById("input")
    input_bar1 = document.getElementById("input2")
    
    sub_btn = document.getElementById("btn")
    if (input_bar.value!="") {
        sub_btn.disabled = false;
    }
    else{
        sub_btn.disabled = true;
    }
    
    if (input_bar1.value!="") {
        sub_btn.disabled = false;
    }
    else{
        sub_btn.disabled = true;
    }
    
}
