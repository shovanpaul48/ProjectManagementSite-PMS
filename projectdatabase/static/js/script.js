
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




document.addEventListener('DOMContentLoaded', function() {
    const logo = document.getElementById('logo');
    const abcElement = document.getElementById('abc');
    const cutButton = document.getElementById('cut-button');

    logo.addEventListener('click', () => {
      if (abcElement.classList.contains('available')) {
        abcElement.classList.remove('available');
        abcElement.classList.add('unavailable');
      } else {
        abcElement.classList.remove('unavailable');
        abcElement.classList.add('available');
      }
    });
    
    cutButton.addEventListener('click', () => {
        if (abcElement.classList.contains('available')) {
          abcElement.classList.remove('available');
          abcElement.classList.add('unavailable');
        } else {
          abcElement.classList.remove('unavailable');
          abcElement.classList.add('available');
        }
      });

  });



// You might also want to add code to show the element when needed
