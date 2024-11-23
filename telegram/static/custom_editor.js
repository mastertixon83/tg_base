document.addEventListener('DOMContentLoaded', function () {
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

    // Функция для создания кнопок с иконками
    function createButton(label, openTag, closeTag, iconClass) {
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

        toolbar.appendChild(button);
    }

    // Добавляем кнопки с иконками
    createButton('Жирный', '<strong>', '</strong>', 'fa-bold');
    createButton('Курсив', '<i>', '</i>', 'fa-italic');
    createButton('Подчёркнутый', '<u>', '</u>', 'fa-underline');
    createButton('Спойлер', '<spoiler>', '</spoiler>', 'fa-eye-slash');
    createButton('Цитата', '<blockquote>', '</blockquote>', 'fa-quote-left');

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
    toolbar.appendChild(linkButton);

    // Вставляем панель кнопок НАД textarea
    const container = editor.closest('.form-row'); // В админке Django элемент для поля textarea
    if (container) {
        container.insertBefore(toolbar, container.firstChild); // Вставляем панель в самое начало контейнера, НАД textarea
    } else {
        console.error('Родительский элемент с классом form-row не найден!');
    }

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
        const tagRegex = new RegExp(`^${openTag}(.*)${closeTag}$`);

        if (tagRegex.test(selectedText)) {
            // Если текст уже обернут в тег, удаляем его
            textarea.value = textarea.value.substring(0, start) + selectedText.slice(openTag.length, -closeTag.length) + textarea.value.substring(end);
        } else {
            // Если тегов нет, добавляем их
            textarea.value = textarea.value.substring(0, start) + wrappedText + textarea.value.substring(end);
        }

        // Восстанавливаем фокус и выделение
        textarea.focus();
        textarea.selectionStart = start + (selectedText.startsWith(openTag) ? 0 : openTag.length);
        textarea.selectionEnd = end + (selectedText.startsWith(openTag) ? 0 : openTag.length);
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
                const linkTag = `<a href="${url}">${selectedText}</a>`;
                textarea.value = textarea.value.substring(0, start) + linkTag + textarea.value.substring(end);
            } else {
                alert('URL не был введен.');
            }
        }

        // Восстанавливаем фокус и выделение
        textarea.focus();
        textarea.selectionStart = start + (selectedText.startsWith('<a href=') ? 0 : 9 + url.length);
        textarea.selectionEnd = textarea.selectionStart + selectedText.length; // Выделяем текст внутри ссылки
    }
});
