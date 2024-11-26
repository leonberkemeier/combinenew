// alert("hy")

showAddCardFormButton = document.getElementById('showAddCardFormButton');
hideAddCardFormButton = document.getElementById('hideAddCard');
AddCardForm = document.getElementById("AddCard");

showAddCardFormButton.addEventListener("click", showCardForm);
hideAddCardFormButton.addEventListener("click", hideCardForm);

function showCardForm(){
    AddCardForm.style.left= `calc(50% - 300px)`;
}

function hideCardForm(){
    AddCardForm.style.left= `-100%`;
}
