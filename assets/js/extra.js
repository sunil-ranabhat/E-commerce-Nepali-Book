
    /* When the user clicks on the button, 
    toggle between hiding and showing the dropdown content */
    function trigger() {
      document.getElementById("myDropdowns").classList.toggle("show");
    }
    
    // Close the dropdown if the user clicks outside of it
    window.onclick = function(event) {
      if (!event.target.matches('.dropbtns')) {
        var dropdowns = document.getElementsByClassName("dropdown-contents");
        var i;
        for (i = 0; i < dropdowns.length; i++) {
          var openDropdown = dropdowns[i];
          if (openDropdown.classList.contains('show')) {
            openDropdown.classList.remove('show');
          }
        }
      }
    }



    function myFunction() {
      var x = document.getElementById("snackbar");
      x.className = "show";
      setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);
    }