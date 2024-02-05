//function to bring out side bar when menu button is pressed
var menu = document.querySelector(".menu-button");

menu.addEventListener("click", function(event) {
    document.querySelector("body").classList.toggle("active");
    event.stopPropagation();
});  

//function to close side bar when any part of the screen is clicked
const sidebar = document.querySelector(".sidebar");
const toggle = document.getElementById("toggle");

document.onclick = function(e) {
    if(!e.target.closest(".sidebar")) {
        document.querySelector("body").classList.remove("active");
    }

} 






