function file_f() {
				var file_input = document.getElementById("file")
				file_input.click();
				
				var file = file_input.files[0]
				var path = URL.createObjectURL(file);

				img = document.getElementById("img");
				img.src = path;                      
}
function changeDp() {
    file_f()
}