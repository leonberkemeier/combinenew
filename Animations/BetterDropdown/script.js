// alert('help')
// animation SKillbar


const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
        console.log(entry)
        if (entry.isIntersecting) {
            entry.target.classList.add('showskillbar');
        } else {
            entry.target.classList.remove('showskillbar');
        }
});
});


const hiddenElements = document.querySelectorAll('.hiddenskillbar');
hiddenElements.forEach((el) => observer.observe(el));



// Show and Hide Collapsibles



const divs = document.querySelectorAll('.collapsible');
// const otherDiv = document.querySelectorAll('.collapsible');

// Add event listener to each div
divs.forEach(div => {
  div.addEventListener('click', function () {
    this.classList.toggle('active');

    var content = this.nextElementSibling;
    if (content.style.display === "block") {
        content.style.display = "none";
    } else {
        content.style.display = "block";
    }

    divs.forEach(otherDiv => {
      if (otherDiv != this) {
        otherDiv.classList.remove('active');
        
        var content = otherDiv.nextElementSibling;
        content.style.display = "none";
      }
    });
  });
});

alert('help');
