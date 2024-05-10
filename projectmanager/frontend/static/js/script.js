
function openNav() {
    document.getElementById("mySidenav").style.width = "250px";
    //document.getElementById("header").style.marginLeft = "250px";
}

function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
    //document.getElementById("header").style.marginLeft= "0";
};

// JavaScript to prevent anchor links from scrolling to the top
document.addEventListener('DOMContentLoaded', function() {
    const anchorLinks = document.querySelectorAll('.card-new');

    anchorLinks.forEach(function(link) {
        link.addEventListener('click', function(event) {
            event.preventDefault(); // Prevent the default behavior of the anchor link

        });
    });
});



