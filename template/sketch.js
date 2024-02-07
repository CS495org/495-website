//function to bring out side bar when menu button is pressed
var menu = document.querySelector(".menu-button");
var overlay = document.querySelector(".overlay");

menu.addEventListener("click", function(event) {
    event.preventDefault(); //don't scroll back to top when button is pressed
    document.querySelector("body").classList.toggle("active");
    overlay.style.display = document.querySelector("body").classList.contains("active") ? "block" : "none"; // Toggle overlay display
    event.stopPropagation();
});  

//function to close side bar when any part of the screen is clicked
const sidebar = document.querySelector(".sidebar");
const toggle = document.getElementById("toggle");

document.onclick = function(e) {
    if(!e.target.closest(".sidebar")) {
        document.querySelector("body").classList.remove("active");
        overlay.style.display = "none"; // Hide overlay when sidebar is closed
    }
} 

//function to highlight the current page the user is on
document.addEventListener("DOMContentLoaded", function() {
    // Get the full URL from the address bar
    var url = window.location.href;

    // Get all <a> tags within the sidebar
    var sidebarLinks = document.querySelectorAll('.sidebar a');

    // Iterate over each <a> tag
    sidebarLinks.forEach(function(link) {
        // Check if the href attribute matches the URL from the address bar
        if (url === link.href) {
            // Add the 'active' class to the closest parent <li> element
            link.closest("li").classList.add("active");
        }
    });
});






