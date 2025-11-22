document.addEventListener('DOMContentLoaded', function() {
    // Валидация форм с проверкой кириллицы и латиницы
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let valid = true;

            // Проверяем каждое обязательное поле
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    valid = false;
                    field.style.borderColor = '#e74c3c';
                    showFieldError(field, 'Это поле обязательно для заполнения');
                } else {
                    field.style.borderColor = '';
                    removeFieldError(field);
                    
                    // Специфическая валидация для разных типов полей
                    if (field.name === 'username') {
                        // Проверяем что логин содержит только латинские буквы и цифры
                        if (!/^[a-zA-Z0-9]+$/.test(field.value)) {
                            valid = false;
                            field.style.borderColor = '#e74c3c';
                            showFieldError(field, 'Логин должен содержать только латинские буквы и цифры');
                        }
                    }
                    
                    // Проверяем что имя и фамилия содержат только кириллические буквы
                    if (field.name === 'first_name' || field.name === 'last_name') {
                        if (!/^[а-яА-ЯёЁ\s]+$/.test(field.value)) {
                            valid = false;
                            field.style.borderColor = '#e74c3c';
                            showFieldError(field, 'Поле должно содержать только кириллические буквы');
                        }
                    }
                }
            });

            if (!valid) {
                e.preventDefault();
            }
        });
    });

    // Функция для показа ошибки под полем
    function showFieldError(field, message) {
        // Удаляем старую ошибку если есть
        removeFieldError(field);
        
        // Создаем элемент с ошибкой
        const errorElement = document.createElement('div');
        errorElement.className = 'field-error';
        errorElement.style.color = '#e74c3c';
        errorElement.style.fontSize = '12px';
        errorElement.style.marginTop = '5px';
        errorElement.textContent = message;
        
        // Вставляем после поля
        field.parentNode.insertBefore(errorElement, field.nextSibling);
    }

    // Функция для удаления ошибки поля
    function removeFieldError(field) {
        const existingError = field.parentNode.querySelector('.field-error');
        if (existingError) {
            existingError.remove();
        }
    }
});