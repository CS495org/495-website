
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


/*document.addEventListener("DOMContentLoaded", function() {
    // Select the parent element that contains all the star icons
    var parentContainer = document.querySelector(".show-placeholder");

    // Add a click event listener to the parent container
    parentContainer.addEventListener("click", function(event) {
        // Check if the clicked element is a star icon
        if (event.target.classList.contains("bx") && event.target.classList.contains("bxs-star")) {
            // Find the closest parent container of the clicked star icon
            var card = event.target.closest(".show-placeholder");
            // Find the corresponding message element within the card
            var message = card.querySelector(".message");
            // Display the corresponding message
            message.style.display = "block";
        }

    });
});*/

/*document.addEventListener("DOMContentLoaded", function() {
    var starIcon = document.querySelector(".star i");
    var message = document.getElementById("message");

    starIcon.addEventListener("click", function(event) {

        // Prevent the default action of the click event on the star icon
        event.preventDefault();

        // Show the message after the star icon is clicked
        message.style.display = "block";
    });
}); */



/*document.querySelectorAll('.star').forEach(function(icon) {
    icon.addEventListener('click', function(event) {
        // Prevent the default action of the icon, such as navigating to a URL
        event.preventDefault();

        // Get the parent show card element of the clicked icon
        var showCard = icon.closest('.show-placeholder');

        showMessage("Added to favorites!");
    });
}); 

function showMessage(message) {
    
    alert(message); 
} */








