document.addEventListener("DOMContentLoaded", function() {
    const phoneInput = document.querySelector('input[name="phone"]'); // ищем по name
    if (!phoneInput) return;

    phoneInput.addEventListener("input", function() {
        let x = phoneInput.value.replace(/\D/g, '').substring(0,11);
        let formatted = '8(';
        if (x.length > 1) formatted += x.substring(1,4);
        if (x.length >= 4) formatted += ')' + x.substring(4,7);
        if (x.length >= 7) formatted += '-' + x.substring(7,9);
        if (x.length >= 9) formatted += '-' + x.substring(9,11);
        phoneInput.value = formatted;
    });
});
