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


/* Functionality to make the check and the star clickable ***************************************
document.querySelectorAll('.star').forEach(function(icon) {
    //initially make all cards unfavorited
    
}); */

// Add event listeners for star icons
document.addEventListener('DOMContentLoaded', function() {


    // Select all star icons and add click event listeners
    document.querySelectorAll('.star').forEach(function(star) {
        star.addEventListener('click', function(event) {
            event.preventDefault(); // Prevent the default link behavior

            const isAuthenticatedValue = document.getElementById('isAuthenticated').value;

            // Convert the string value to a boolean
            const isAuthenticated = isAuthenticatedValue === 'true';
            // If the user is not authenticated, redirect to the login page
            if (!isAuthenticated) {
                window.location.href = 'https://localhost/accounts/login/'; // Adjust the URL as per your login page URL
                return; // Stop further execution
            }


            const showId = this.getAttribute('data-show-id'); // Get the show ID
            const title = this.getAttribute('data-show-title'); //Get the show title
            const starIcon = this.querySelector('i');
            starIcon.classList.toggle('favorited');
            
            // Send an AJAX request to favorite the show
            fetch(`https://localhost/tv-manager/ajax_update_fav_shows/${showId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCSRFToken(), // Get the CSRF token
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ showId: showId }), // Include the show ID in the request body
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Failed to favorite the show');
                }
                return response.json();
            })
            .then(data => {
                const action = data.action;
                const fav_show_ids = data.fav_show_ids; // Assuming this is how you receive fav_show_ids from the server

                console.log('fav_show_ids:', fav_show_ids);

                if (action === 'added') {
                    alert(`${title} has been added to favorites!`);
                    starIcon.classList.add('favorited');
                }
                else if (action === 'removed'){
                    alert(`${title} has been removed from favorites!`);
                    starIcon.classList.remove('favorited');
                }

            })
            .catch(error => {
                console.error('Error:', error);
                // Handle errors (e.g., display error message to the user)
            });

        });
    });
});



// Function to get the CSRF token from the form
function getCSRFToken() {
    const csrfTokenElement = document.querySelector('[name=csrfmiddlewaretoken]');
    if (csrfTokenElement) {
        return csrfTokenElement.value;
    } else {
        console.error('CSRF token not found');
        return null;
    }
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

/*function reloadPage() {
    // Perform a hard reload of the page
    window.location.reload(true);
} */




