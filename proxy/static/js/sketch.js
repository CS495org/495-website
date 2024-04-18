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



//FETCH FOR THE STAR CLICK *********************************************************************************************
document.addEventListener('DOMContentLoaded', async function() {
    // Select all star icons and add click event listeners
    document.querySelectorAll('.star').forEach(function(star) {
        star.addEventListener('click', async function(event) {
            event.preventDefault(); // Prevent the default link behavior

            const isAuthenticatedValue = document.getElementById('isAuthenticated').value;
            const isAuthenticated = isAuthenticatedValue === 'true';
            
            if (!isAuthenticated) {
                window.location.href = 'https://localhost/accounts/login/';
                return;
            }

            const showId = this.getAttribute('data-show-id');
            const title = this.getAttribute('data-show-title');
            const starIcon = this.querySelector('i');
            starIcon.classList.toggle('favorited');

            let firstFetchSuccessful = false;
            
            try {
                const response = await fetch(`https://localhost/tv-manager/ajax_update_fav_shows/${showId}/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCSRFToken(),
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ showId: showId }),
                });

                if (!response.ok) {
                    throw new Error('Failed to favorite the show');
                }

                const data = await response.json();
                const action = data.action;
                const fav_show_ids = data.fav_show_ids;

                console.log('fav_show_ids:', fav_show_ids);
                firstFetchSuccessful = true;

                if (action === 'added') {
                    alert(`${title} has been added to favorites!`);
                    starIcon.classList.add('favorited');
                } else if (action === 'removed') {
                    alert(`${title} has been removed from favorites!`);
                    starIcon.classList.remove('favorited');
                }

                window.location.reload();
                

                
            } catch (error) {
                console.error('Error:', error);
                // Handle errors (e.g., display error message to the user)
            }

            console.log('First fetch successful:', firstFetchSuccessful);


            if(!firstFetchSuccessful) {
                try {
                    const secondResponse = await fetch(`https://localhost/tv-manager/ajax_update_fav_top/${showId}/`, {
                        method: 'POST',
                        headers: {
                            'X-CSRFToken': getCSRFToken(),
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ showId: showId }),
                    });
    
                    if (!secondResponse.ok) {
                        throw new Error('Failed to favorite the show');
                    }
    
                    const second_data = await secondResponse.json();
                    const action_fav_top = second_data.action_fav_top;
                    const fav_top_ids = second_data.fav_top_ids;
    
                    console.log('fav_top_ids:', fav_top_ids);
                   // firstFetchSuccessful = true;
    
                    if (action_fav_top === 'added') {
                        alert(`${title} has been added to favorites!`);
                        starIcon.classList.add('favorited');
                    } else if (action_fav_top === 'removed') {
                        alert(`${title} has been removed from favorites!`);
                        starIcon.classList.remove('favorited');
                    }

                  //  const scrollPosition = window.scrollY || window.pageYOffset;
                    // Reload the page
                    window.location.reload();
                    // Restore the scroll position after the page reloads
                   // window.scrollTo(0, scrollPosition); 
    
                    
                } catch (error) {
                    console.error('Error:', error);
                    // Handle errors (e.g., display error message to the user)
                } 
            }  



        });
    });
});

//FETCH FOR THE CHECK CLICK **************************************************************************************************
document.addEventListener('DOMContentLoaded', async function() {
    // Select all check icons and add click event listeners
    document.querySelectorAll('.check').forEach(function(check) {
        check.addEventListener('click', async function(event) {
            event.preventDefault(); // Prevent the default link behavior

            const isAuthenticatedValue = document.getElementById('isAuthenticated').value;
            const isAuthenticated = isAuthenticatedValue === 'true';
            
            if (!isAuthenticated) {
                window.location.href = 'https://localhost/accounts/login/';
                return;
            }

            const showId = this.getAttribute('data-show-id');
            const title = this.getAttribute('data-show-title');
            const checkIcon = this.querySelector('i');
            checkIcon.classList.toggle('completed');

            let firstFetchSuccessful = false;
            
            try {
                const response = await fetch(`https://localhost/tv-manager/ajax_update_comp_shows/${showId}/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCSRFToken(),
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ showId: showId }),
                });

                if (!response.ok) {
                    throw new Error('Failed to mark show as completed');
                }

                const data = await response.json();
                const action_comp_show = data.action_comp_show;
                const comp_show_ids = data.comp_show_ids;

                console.log('comp_show_ids:', comp_show_ids);
                firstFetchSuccessful = true;

                if (action_comp_show === 'added') {
                    alert(`${title} has been added to completed!`);
                    checkIcon.classList.add('completed');
                } else if (action_comp_show === 'removed') {
                    alert(`${title} has been removed from completed!`);
                    checkIcon.classList.remove('completed');
                }

                window.location.reload();
                

                
            } catch (error) {
                console.error('Error:', error);
                // Handle errors (e.g., display error message to the user)
            }

            console.log('First fetch successful:', firstFetchSuccessful);


            if(!firstFetchSuccessful) {
                try {
                    const secondResponse = await fetch(`https://localhost/tv-manager/ajax_update_comp_top/${showId}/`, {
                        method: 'POST',
                        headers: {
                            'X-CSRFToken': getCSRFToken(),
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ showId: showId }),
                    });
    
                    if (!secondResponse.ok) {
                        throw new Error('Failed to mark show as completed');
                    }
    
                    const second_data = await secondResponse.json();
                    const action_comp_top = second_data.action_comp_top;
                    const comp_top_ids = second_data.comp_top_ids;
    
                    console.log('comp_top_ids:', comp_top_ids);
                   // firstFetchSuccessful = true;
    
                    if (action_comp_top === 'added') {
                        alert(`${title} has been added to completed!`);
                        checkIcon.classList.add('completed');
                    } else if (action_comp_top === 'removed') {
                        alert(`${title} has been removed from completed!`);
                        checkIcon.classList.remove('completed');
                    }

                  //  const scrollPosition = window.scrollY || window.pageYOffset;
                    // Reload the page
                    window.location.reload();
                    // Restore the scroll position after the page reloads
                   // window.scrollTo(0, scrollPosition); 
    
                    
                } catch (error) {
                    console.error('Error:', error);
                    // Handle errors (e.g., display error message to the user)
                } 
            }  



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







