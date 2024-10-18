import os
import requests

from django.db import models
from django.utils import timezone
from django.utils.html import mark_safe
from django.utils.text import slugify
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

from PIL import Image
from io import BytesIO


class Admin(models.Model):
    """Класс описания модели Админа канала"""
    nickname = models.CharField(verbose_name="Админ канала", max_length=150)
    name = models.CharField(verbose_name="Имя", max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Админ канала"
        verbose_name_plural = "Админы каналов"


class Category(models.Model):
    """Класс описания модели категорий"""
    category = models.CharField(verbose_name="Категория", max_length=150)

    def __str__(self):
        return self.category

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категрии"


class Channel(models.Model):
    """Класс описания модели канала"""
    title = models.CharField(verbose_name="Название канала", max_length=255)
    description = models.TextField(verbose_name="Описание канала")
    url = models.URLField(verbose_name="Ссылка на канал")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='channels')
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE, related_name="channel_admin")
    created_at = models.DateField(verbose_name="Дата создания канала")
    gpt_prompt = models.TextField(verbose_name="Промпт для GPT", blank=True, null=True, default=None)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Канал"
        verbose_name_plural = "Каналы"


class Button(models.Model):
    """Класс описания модели кнопок"""
    text = models.CharField(verbose_name="Текст на кнопке", max_length=90, blank=True, null=True, default=None)
    link = models.URLField(verbose_name="Ссылка", blank=True, null=True, default=None)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='button')

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Кнопка"
        verbose_name_plural = "Кнопки"


class Post(models.Model):
    """Класс описания модели поста"""
    ADS = "A"
    CREO = "C"
    POST = "P"
    POST_TYPES = [
        (ADS, "Реклама"),
        (CREO, "Креатив"),
        (POST, "Пост")
    ]

    created_at = models.DateTimeField(verbose_name="Дата создания поста", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Дата изменения", auto_now=True)
    text = models.TextField(verbose_name="Текст поста")
    comment = models.TextField(verbose_name="Комментарий", blank=True, null=True, default=None)
    article = models.CharField(verbose_name="Артикул", default=None, blank=True, null=True)
    channel = models.ForeignKey(
        Channel,
        on_delete=models.CASCADE,
        related_name='contents',
        null=True,
        blank=True
    )
    post_data = models.DateField(verbose_name="Дата публикации", null=True, blank=True, default=None)
    post_time = models.TimeField(verbose_name="Время публикации", null=True, blank=True, default=None)
    status = models.BooleanField(verbose_name="Опубликован", default=False)
    date_time_publication = models.DateTimeField(verbose_name="Дата и время публикации", null=True, blank=True, default=None)
    post_type = models.CharField(verbose_name="Тип поста", max_length=1, choices=POST_TYPES, blank=False,
                                    null=False, default=POST)
    message_id = models.TextField(verbose_name="ID сообщения", blank=True, null=True, default=None)
    ads_status = models.BooleanField(verbose_name="Статус рекламного поста", default=True)
    product_category = models.CharField(verbose_name="Категория товара", blank=True, null=True, default=None)

    @property
    def category(self):
        return self.channel.category

    def __str__(self):
        return f"{self.id} - {self.text[:200]}"

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        ordering = ["-pk"]


class BotToken(models.Model):
    """Класс модели токенов ботов"""
    token = models.CharField(verbose_name="Токен бота", max_length=250, blank=True, null=True, unique=True)
    name = models.CharField(verbose_name="Имя бота", max_length=150, blank=True, null=True)
    channel = models.ForeignKey(
        Channel,
        on_delete=models.SET_NULL,
        related_name='bot_tokens',
        null=True,
        blank=True
    )
    chat_id = models.CharField(verbose_name="Id Канала", max_length=150, blank=True, null=True, default=None)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Бот постер"
        verbose_name_plural = "Боты постеры"


def media_upload_to(instance, filename):
    post_id = instance.post.id if instance.post and instance.post.id else 'unsaved_post'
    # filename = slugify(filename)
    return os.path.join('media', str(post_id), filename)


class Media(models.Model):
    """Класс описания модели Медиа"""
    file = models.FileField(verbose_name="Файл", upload_to=media_upload_to, blank=True, null=True)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='media_files')
    created_at = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True, null=True, blank=True)
    file_url = models.URLField(verbose_name="URL файла", blank=True, null=True)  # Добавляем поле для URL
    spoiler = models.BooleanField(verbose_name="Спойлер", default=False)

    def __str__(self):
        return self.file.name

    def preview(self):
        if self.file:
            # Добавляем HTML-ссылку с `target="_blank"`, чтобы открывалась в новой вкладке
            return mark_safe(
                f'<a href="{self.file.url}" target="_blank"><img src="{self.file.url}" style="width: 100px; height: auto;" /></a>')
        return ""

    class Meta:
        verbose_name = "Медиафайл"
        verbose_name_plural = "Медиафайлы"

    def delete(self, *args, **kwargs):
        """Удаление файла при удалении записи из таблицы"""
        if self.file and os.path.isfile(self.file.path):
            os.remove(self.file.path)
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        """Переопределяем сохранение для загрузки файла по URL"""
        if self.file_url and not self.file:
            self.save_file_from_url(self.file_url)
            self.file_url = None  # Очищаем URL после загрузки
        super().save(*args, **kwargs)

    def save_file_from_url(self, url):
        """Загрузка файла по URL и сохранение его в поле file"""
        response = requests.get(url)
        if response.status_code == 200:
            file_name = os.path.basename(url)
            file_ext = os.path.splitext(file_name)[1].lower()

            if file_ext == '.webp':  # Если файл webp, конвертируем его в jpg
                img = Image.open(BytesIO(response.content))
                img = img.convert("RGB")  # Преобразуем в RGB, т.к. jpg не поддерживает альфа-канал

                # Генерируем новое имя файла с расширением jpg
                file_name = os.path.splitext(file_name)[0] + '.jpg'

                # Создаем временный файл
                temp_file = NamedTemporaryFile(suffix='.jpg', delete=True)
                img.save(temp_file, format='JPEG')
                temp_file.flush()

                # Сохраняем конвертированный файл в поле file
                self.file.save(file_name, File(temp_file), save=False)
            else:
                # Для других форматов сохраняем без изменений
                # Если у файла нет расширения, добавляем исходное расширение
                if not file_ext:
                    file_name += '.bin'  # Подумайте о назначении расширения по умолчанию

                temp_file = NamedTemporaryFile(delete=True)
                temp_file.write(response.content)
                temp_file.flush()
                self.file.save(file_name, File(temp_file), save=False)
        else:
            raise Exception("Не удалось загрузить файл с указанного URL")


@receiver(post_delete, sender=Media)
def delete_media_file(sender, instance, **kwargs):
    """Удаление медиафайла при удалении объекта"""
    if instance.file:
        file_path = instance.file.path
        directory = os.path.dirname(file_path)

        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)

        # Проверяем, пуста ли директория после удаления файла
        if not os.listdir(directory):  # Если директория пуста
            os.rmdir(directory)  # Удаляем директорию


@receiver(pre_save, sender=Media)
def delete_old_media_file(sender, instance, **kwargs):
    """Удаление старого файла при обновлении записи"""
    if not instance.pk:
        return False

    try:
        old_file = Media.objects.get(pk=instance.pk).file
    except Media.DoesNotExist:
        return False

    new_file = instance.file
    if old_file != new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)


