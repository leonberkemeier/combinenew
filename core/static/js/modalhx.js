alert('hi');

FrontCard=document.getElementById("frontcard");
BackCard=document.getElementById("backcard");
ToggleButton=document.getElementById("toggle-button");


ToggleButton.addEventListener("click", toggleCards);


function toggleCards(){
    FrontCard.classList.toggle("show-card");
    BackCard.classList.toggle("show-card");
}



