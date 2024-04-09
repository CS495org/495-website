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

// Function for handling the calendar logic
document.addEventListener('DOMContentLoaded', function() {
    const calendarIcon = document.getElementById('calendarIcon');
    const calendarWindow = document.getElementById('calendarWindow');

    if (!calendarIcon || !calendarWindow) {
        console.error('Calendar elements not found!');
        return; // Stop the function if elements are not found
    }

    // Function to toggle the display of the calendar window
    function toggleCalendar() {
        calendarWindow.style.display = (calendarWindow.style.display === "none") ? "block" : "none";
        if (calendarWindow.style.display === "block") {
            generateCalendar(); // Call function to generate calendar content
        }
    }

    // Function to generate the calendar content dynamically
    function generateCalendar() {
        // Check if the calendar was already generated to avoid regenerating it every click
        if (!calendarWindow.querySelector('.simple-calendar')) {
            calendarWindow.innerHTML = '<div class="simple-calendar">Simple Calendar Placeholder</div>';
            // Future expansion: generate current month's calendar dynamically
        }
    }

    calendarIcon.addEventListener('click', toggleCalendar);
});





/* Functionality to make the check and the star clickable ***************************************/
document.querySelectorAll('.star').forEach(function(icon) {
    //initially make all cards unfavorited
    var isFavorite = false;

    icon.addEventListener('click', function(event) {
        // Prevent the default action of the icon, such as navigating to a URL
        event.preventDefault();

        // Toggle the 'clicked' class for the clicked star icon
        icon.classList.toggle('clicked');

        // Get the parent show card element of the clicked icon
        var showCard = icon.closest('.show-placeholder');

        if (isFavorite) {
            // If it's currently favorited, display an unfavorited message
            showMessage("Removed from favorites!");
        } else {
            // If it's currently unfavorited, display a favorited message
            showMessage("Added to favorites!");
        }

        isFavorite = !isFavorite;
    });
}); 

function showMessage(message) {
    alert(message); 
} 


document.querySelectorAll('.check').forEach(function(icon) {
    //initially make all cards unfavorited
    var isComplete = false;

    icon.addEventListener('click', function(event) {
        // Prevent the default action of the icon, such as navigating to a URL
        event.preventDefault();

        // Toggle the 'clicked' class for the clicked star icon
        icon.classList.toggle('clicked');

        // Get the parent show card element of the clicked icon
        var showCard = icon.closest('.show-placeholder');

        if (isComplete) {
            // If it's currently favorited, display an unfavorited message
            showMessage("Removed from completed!");
        } else {
            // If it's currently unfavorited, display a favorited message
            showMessage("Added to completed!");
        }

        isComplete = !isComplete;
    });
}); 

function showMessage(message) {
    alert(message); 
} 





