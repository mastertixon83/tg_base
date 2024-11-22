CKEDITOR.plugins.add('spoiler', {
    icons: 'spoiler',
    init: function(editor) {
        // Подключаем стили плагина
        editor.addContentsCss(CKEDITOR.plugins.getPath('spoiler') + 'spoiler.css');

        // Добавляем команду для переключения спойлера
        editor.addCommand('toggleSpoiler', {
            exec: function(editor) {
                var selection = editor.getSelection();
                var range = selection.getRanges()[0];

                if (!range) {
                    alert('Выдели текст для добавления/удаления спойлера.');
                    return;
                }

                var startElement = selection.getStartElement();

                if (startElement && startElement.getName() === 'spoiler') {
                    var textInsideSpoiler = startElement.getText(); // Сохраняем текст внутри тега <spoiler>
                    var parent = startElement.getParent();

                    // Создаем текстовый узел
                    var textNode = new CKEDITOR.dom.text(textInsideSpoiler, editor.document);

                    // Вставляем текстовый узел перед <spoiler>
                    startElement.insertBeforeMe(textNode);

                    // Удаляем тег <spoiler>
                    startElement.remove();
                } else {
                    // Если текст не внутри <spoiler>, оборачиваем его в тег <spoiler>
                    var selectedText = selection.getSelectedText();
                    if (selectedText) {
                        var spoilerElement = editor.document.createElement('spoiler');
                        spoilerElement.setText(selectedText);

                        range.deleteContents(); // Удаляем текущий выделенный текст
                        range.insertNode(spoilerElement); // Вставляем тег <spoiler> с текстом
                    } else {
                        alert('Выдели текст для добавления/удаления спойлера.');
                    }
                }
            }
        });

        // Добавляем кнопку в панель инструментов
        editor.ui.addButton('Spoiler', {
            label: 'Спрятать текст под мпойлер',
            command: 'toggleSpoiler',
            toolbar: 'insert',
            icon: 'spoiler'
        });

        // Обработчик для обновления состояния кнопки (выключение/включение)
        editor.on('selectionChange', function() {
            var selection = editor.getSelection();
            var startElement = selection.getStartElement();

            // Включаем или выключаем кнопку в зависимости от того, находится ли курсор внутри тега <spoiler>
            if (startElement && startElement.getName() === 'spoiler') {
                editor.getCommand('toggleSpoiler').setState(CKEDITOR.TRISTATE_ON);
            } else {
                editor.getCommand('toggleSpoiler').setState(CKEDITOR.TRISTATE_OFF);
            }
        });
    }
});
