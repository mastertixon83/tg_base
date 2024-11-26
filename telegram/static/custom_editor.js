document.addEventListener("DOMContentLoaded", function () {
    // *** Ответственное за поле post_type и управление полем answers ***
    const postTypeField = document.querySelector("#id_post_type"); // Поле выбора post_type
    const answersFieldContainer = document.querySelector(".form-row.field-answers"); // Контейнер для поля answers

    // Функция для управления видимостью поля answers
    function toggleAnswersField() {
        if (postTypeField.value === "Q" || postTypeField.value === "M") {
            answersFieldContainer.style.display = ""; // Показываем поле
        } else {
            answersFieldContainer.style.display = "none"; // Скрываем поле
        }
    }

    // Выполняем проверку при загрузке страницы
    toggleAnswersField();

    // Выполняем проверку при изменении значения post_type
    postTypeField.addEventListener("change", toggleAnswersField);

    // *** Ответственное за кастомный редактор текста ***
    const editor = document.getElementById('editor'); // Получаем textarea по ID

    if (!editor) {
        console.error('Textarea с указанным ID не найдено!');
        return;
    }

    // Создаем контейнер для панели кнопок
    const toolbar = document.createElement('div');
    toolbar.classList.add('custom-toolbar'); // Для кастомной стилизации
    toolbar.style.textAlign = 'center';  // Центрируем кнопки в панели
    toolbar.style.marginBottom = '10px';  // Отступ снизу для панельки

    // Функция для создания кнопок с иконками и подсказками
    function createButton(label, openTag, closeTag, iconClass, tooltip) {
        const button = document.createElement('button');
        button.type = 'button';
        button.style.marginRight = '5px'; // Отступ между кнопками
        button.onclick = function () {
            wrapText(editor, openTag, closeTag);
        };

        // Создаем иконку и добавляем ее в кнопку
        const icon = document.createElement('i');
        icon.classList.add('fas', iconClass);  // Добавляем иконку через FontAwesome
        button.appendChild(icon);

        // Добавляем подсказку (title) при наведении на кнопку
        button.setAttribute('title', tooltip);

        toolbar.appendChild(button);
    }

    // Добавляем кнопки с иконками и подсказками
    createButton('Жирный', '<b>', '</b>', 'fa-bold', 'Жирный текст');
    createButton('Курсив', '<i>', '</i>', 'fa-italic', 'Курсивный текст');
    createButton('Подчёркнутый', '<u>', '</u>', 'fa-underline', 'Подчеркнутый текст');
    createButton('Спойлер', '<spoiler>', '</spoiler>', 'fa-eye-slash', 'Спойлер');
    createButton('Цитата', '<blockquote>', '</blockquote>', 'fa-quote-left', 'Цитата');

    // Кнопка для создания ссылки
    const linkButton = document.createElement('button');
    linkButton.type = 'button';
    linkButton.style.marginRight = '5px';
    linkButton.onclick = function () {
        toggleLink(editor);
    };

    // Иконка для кнопки "Ссылка"
    const linkIcon = document.createElement('i');
    linkIcon.classList.add('fas', 'fa-link');  // Иконка для ссылки
    linkButton.appendChild(linkIcon);

    // Добавляем подсказку для кнопки "Ссылка"
    linkButton.setAttribute('title', 'Вставить ссылку');

    toolbar.appendChild(linkButton);

    // Вставляем панель кнопок НАД textarea
    const container = editor.closest('.form-row'); // В админке Django элемент для поля textarea
    if (container) {
        container.insertBefore(toolbar, container.firstChild); // Вставляем панель в самое начало контейнера, НАД textarea
    } else {
        console.error('Родительский элемент с классом form-row не найден!');
    }

    // Создаем контейнер для счётчика символов
    const charCounter = document.createElement('div');
    charCounter.id = 'char-counter'; // Уникальный ID для счётчика
    charCounter.classList.add('char-counter');
    charCounter.style.textAlign = 'left';
    charCounter.style.marginTop = '5px';
    charCounter.style.fontSize = '14px';

    // Добавляем счётчик под textarea
    if (container) {
        container.appendChild(charCounter);
    }

    // Функция для обновления счётчика символов
    function updateCharCounter() {
        const charCount = editor.value.length;
        let maxCount = 1024;
        if (postTypeField.value === "Q" || postTypeField.value === "M") {
            maxCount = 300;
        }
        charCounter.textContent = `Количество символов: ${charCount} - Максимум ${maxCount}`;

        // Изменяем цвет текста счётчика
        charCounter.style.color = charCount > maxCount ? 'red' : '#fff';
    }

    // Обновляем счётчик при вводе текста вручную
    editor.addEventListener('input', updateCharCounter);

    // Устанавливаем начальное значение счётчика
    updateCharCounter();

    // Функция для оборачивания/удаления текста в теги
    function wrapText(textarea, openTag, closeTag) {
        const start = textarea.selectionStart;
        const end = textarea.selectionEnd;

        if (start === end) {
            alert('Выберите текст для оборачивания.');
            return;
        }

        const selectedText = textarea.value.substring(start, end);
        const wrappedText = openTag + selectedText + closeTag;

        // Регулярные выражения для проверки, обернут ли текст в теги
        const tagRegex = new RegExp('^${openTag}(.*)${closeTag}$');

        if (tagRegex.test(selectedText)) {
            // Если текст уже обернут в тег, удаляем его
            textarea.value = textarea.value.substring(0, start) + selectedText.slice(openTag.length, -closeTag.length) + textarea.value.substring(end);
        } else {
            // Если тегов нет, добавляем их
            textarea.value = textarea.value.substring(0, start) + wrappedText + textarea.value.substring(end);
        }

        // Восстанавливаем фокус и выделение
        textarea.focus();
        textarea.selectionStart = start + openTag.length;
        textarea.selectionEnd = end + openTag.length;

        // Пересчёт символов
        updateCharCounter();
    }

    // Функция для создания или удаления ссылки
    function toggleLink(textarea) {
        const start = textarea.selectionStart;
        const end = textarea.selectionEnd;

        if (start === end) {
            alert('Выберите текст для создания или удаления ссылки.');
            return;
        }

        const selectedText = textarea.value.substring(start, end);

        // Проверяем, обернут ли выделенный текст в тег <a>
        const linkRegex = /^<a href="[^"]+">(.+)<\/a>$/;
        if (linkRegex.test(selectedText)) {
            // Если текст обернут в ссылку, удаляем тег <a>
            const unwrappedText = selectedText.replace(linkRegex, '$1');
            textarea.value = textarea.value.substring(0, start) + unwrappedText + textarea.value.substring(end);
        } else {
            // Если текст не обернут в ссылку, добавляем тег <a>
            const url = prompt('Введите URL для ссылки:');
            if (url) {
                const linkTag = '<a href="${url}">${selectedText}</a>';
                textarea.value = textarea.value.substring(0, start) + linkTag + textarea.value.substring(end);
            } else {
                alert('URL не был введен.');
            }
        }

        // Восстанавливаем фокус и выделение
        textarea.focus();
        updateCharCounter();
    }
});