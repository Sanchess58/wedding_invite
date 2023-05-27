counter = 0;
active = true;

function addbtn(){
    if (active == true){
        const addBtn = document.querySelector('.addBtn');
        const createDiv = document.createElement('div');
        const createInput = document.createElement('input');
        createDiv.className = 'form_group';
        createInput.className = 'form_input';
        createInput.id = 'name';
        createInput.name = 'name';
        createInput.type = 'text'; 
        createDiv.appendChild(createInput).placeholder = 'Введите ФИО гостя';  
        addBtn.insertAdjacentElement('beforebegin', createDiv);
        counter++;
        if (counter > 9) {
            active = false;
            alert("Больше гостей добавить нельзя!")
        }
    }
}



