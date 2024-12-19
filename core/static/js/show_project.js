// alert("hy")

showAddCardFormButton = document.getElementById('showAddCardFormButton');
hideAddCardFormButton = document.getElementById('hideAddCard');
AddCardForm = document.getElementById("AddCard");

showAddCardFormButton.addEventListener("click", showCardForm);
hideAddCardFormButton.addEventListener("click", hideCardForm);

var w = window.innerWidth;
console.log("viewPortWithd: " + w);


showModalButton = document.getElementById('show-modal');
hideModalButton = document.getElementById('close-modal');
Modal = document.getElementById('containerModal');

showModalButton.addEventListener("click", showModal);
hideModalButton.addEventListener("click", hideModal);

function showCardForm(){
    AddCardForm.classList.add("show-modal")
    Modal.classList.remove("show-modal");
}

function hideCardForm(){
    AddCardForm.classList.remove("show-modal");    
}


function showModal(){
    
    Modal.classList.add("show-modal");
    AddCardForm.classList.remove("show-modal");
}

function hideModal(){
    Modal.classList.remove("show-modal");
}