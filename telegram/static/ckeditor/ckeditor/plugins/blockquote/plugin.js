CKEDITOR.plugins.add('blockquote', {
    icons: 'blockquote',
    init: function(editor) {
        // Подключаем стили плагина
        editor.addContentsCss(CKEDITOR.plugins.getPath('blockquote') + 'blockquote.css');

        // Добавляем команду для переключения спойлера
        editor.addCommand('toggleBlockquote', {
            exec: function(editor) {
                var selection = editor.getSelection();
                var range = selection.getRanges()[0];

                if (!range) {
                    alert('Выдели текст для добавления/удаления спойлера.');
                    return;
                }

                var startElement = selection.getStartElement();

                if (startElement && startElement.getName() === 'blockquote') {
                    var textInsideBlockquote = startElement.getText(); // Сохраняем текст внутри тега <spoiler>
                    var parent = startElement.getParent();

                    // Создаем текстовый узел
                    var textNode = new CKEDITOR.dom.text(textInsideBlockquote, editor.document);

                    // Вставляем текстовый узел перед <spoiler>
                    startElement.insertBeforeMe(textNode);

                    // Удаляем тег <spoiler>
                    startElement.remove();
                } else {
                    // Если текст не внутри <spoiler>, оборачиваем его в тег <spoiler>
                    var selectedText = selection.getSelectedText();
                    if (selectedText) {
                        var blockquoteElement = editor.document.createElement('blockquote');
                        blockquoteElement.setText(selectedText);

                        range.deleteContents(); // Удаляем текущий выделенный текст
                        range.insertNode(blockquoteElement); // Вставляем тег <spoiler> с текстом
                    } else {
                        alert('Выдели текст для добавления/удаления тега.');
                    }
                }
            }
        });

        // Добавляем кнопку в панель инструментов
        editor.ui.addButton('Blockquote', {
            label: 'Цитировать текст',
            command: 'toggleBlockquote',
            toolbar: 'insert',
            icon: 'blockquote'
        });

        // Обработчик для обновления состояния кнопки (выключение/включение)
        editor.on('selectionChange', function() {
            var selection = editor.getSelection();
            var startElement = selection.getStartElement();

            // Включаем или выключаем кнопку в зависимости от того, находится ли курсор внутри тега <spoiler>
            if (startElement && startElement.getName() === 'blockquote') {
                editor.getCommand('toggleBlockquote').setState(CKEDITOR.TRISTATE_ON);
            } else {
                editor.getCommand('toggleBlockquote').setState(CKEDITOR.TRISTATE_OFF);
            }
        });
    }
});
