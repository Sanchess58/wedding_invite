function validatePhone(phone){
    let regex = /^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$/;
    return regex.test(phone);
}
function error_or_thanks() {
    jQuery('.form_group').addClass('js-close');
    jQuery('.button_form').addClass('js-close');
    jQuery('#thanks').removeClass('js-close');
}
function get_arr() {   
    is_good = true;
    arr = [];
    const onlyInputsName = document.querySelectorAll('.registration_form #name');
    const onlyInputPhone = document.querySelector('.registration_form #phone');

    onlyInputsName.forEach(input => {
        arr.push(input.value);
    });
    if (!validatePhone(onlyInputPhone.value.trim())){
        is_good = false;
        jQuery('#error').removeClass('js-close');
        
      }
    if (is_good) {
        $.ajax({
            url: "/",
            type: "POST",
            data : {
                name: arr, 
                phone: onlyInputPhone.value.trim(),
            }, 
            success: function(dat) { 
                error_or_thanks();
            },
            error: function(dat,ts){
                alert("Произошла непредвиденная ошибка!");
            },
        });
    }
}