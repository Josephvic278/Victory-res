function file_f() {
				var file_input = document.getElementById("file")
				file_input.click();
				
				var file = file_input.files[0]
				var path = URL.createObjectURL(file);

				img = document.getElementById("img");
				img.src = path;
       filename = file.name;
       
       var a = document.getElementById("a")
       a.href=path;
       a.download=filename;
       
       document.getElementById("user_dp").value=filename
       a.click();
}
function changeDp() {
    file_f()
}