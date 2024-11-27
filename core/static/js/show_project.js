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
    AddCardForm.style.left= `-601px`;
}

showModalButton = document.getElementById('show-modal');
hideModalButton = document.getElementById('close-modal');
Modal = document.getElementById('containerModal');

showModalButton.addEventListener("click", showModal);
hideModalButton.addEventListener("click", hideModal);

function showModal(){
    Modal.style.right = 'calc(50% - calc(var(--modal-heigt) * 2 + 10px))';
}

function hideModal(){
    Modal.style.right = `calc( -1 * calc(var(--modal-heigt) * 4 + 20px))`;
}