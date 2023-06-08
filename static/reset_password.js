function runCountDown() {
    let v = document.getElementById("counter");
    let i = parseInt(v.textContent);
    
    if (i > 0) {
        i--;
        v.textContent = i;
    }
}

setInterval(runCountDown, 1000);
