
    function processIntersectionEntries(entries) {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.classList.add("back-to-top-container--intersecting");
          } else {
            entry.target.classList.remove("back-to-top-container--intersecting");
          }
        });
      }
    window.addEventListener("load", function(event) {
        var element = document.querySelector(".back-to-top-container");
        var intersectionObserver;
        
        intersectionObserver = new IntersectionObserver(processIntersectionEntries);
        intersectionObserver.observe(element);
      }, false);

