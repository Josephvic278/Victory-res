function openUserProfile() {
    var userProfile = document.getElementById("userProfile")
    userProfile.style.display="block";
    
    var menuBar = document.getElementById('menuBar')    
    menuBar.style.display='none';
}

function closeUserProfile(){
    var userProfile = document.getElementById('userProfile');
    userProfile.style.display='none';

    var menuBar = document.getElementById('menuBar')    
    menuBar.style.display='block'; 
}