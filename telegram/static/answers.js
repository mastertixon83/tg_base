document.addEventListener("DOMContentLoaded", function () {
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
});