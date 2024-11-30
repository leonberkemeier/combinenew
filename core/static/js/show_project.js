// alert("hy")

showAddCardFormButton = document.getElementById('showAddCardFormButton');
hideAddCardFormButton = document.getElementById('hideAddCard');
AddCardForm = document.getElementById("AddCard");

showAddCardFormButton.addEventListener("click", showCardForm);
hideAddCardFormButton.addEventListener("click", hideCardForm);


showModalButton = document.getElementById('show-modal');
hideModalButton = document.getElementById('close-modal');
Modal = document.getElementById('containerModal');

showModalButton.addEventListener("click", showModal);
hideModalButton.addEventListener("click", hideModal);

function showCardForm(){
    AddCardForm.style.left= `calc(50% - 300px)`;
    Modal.style.left = `calc( -1 * calc(var(--modal-heigt) * 4 + 20px + 40px))`;
}

function hideCardForm(){
    AddCardForm.style.left= `-601px`;
}


function showModal(){
    Modal.style.left = 'calc(50% - calc(var(--modal-heigt) * 2 + 10px))';
    AddCardForm.style.left= `-601px`;
}

function hideModal(){
    Modal.style.left = `calc( -1 * calc(var(--modal-heigt) * 4 + 20px + 40px))`;
}