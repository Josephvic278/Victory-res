function open_close_post_bar() {
				var op_cl = document.getElementById("open_bar")
				op_cl.style.display = "block"
}

function close_bar() {
				var close_bar = document.getElementById("open_bar")
				close_bar.style.display = "none"
}


function file_f() {
				var file_input = document.getElementById("file")
				var file = file_input.files[0]
				var path = URL.createObjectURL(file);

				img = document.getElementById("img");
				img.src = path;
				
				send_img = document.getElementById("send_img");
				send_img.value=path;

}
