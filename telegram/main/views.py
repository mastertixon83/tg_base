from django.shortcuts import render
from django.conf import settings

from loguru import logger
import transliterate
import re
from .models import *

from utils.parser_wb.parser import run_parser_wb, run_parser_tg


def home_view(request):
    """Вывод главной стрницы"""
    channels = Channel.objects.all()
    # Возвращаем объекты страницы вместе с пагинатором в контексте
    return render(request, 'main/index.html', {'title': 'Главная', 'user': request.user, "channels": channels})


def get_channel_prompt(request, pk):
    """Возвращает промпт для канала для GPT"""
    channel = Channel.objects.get(pk=pk)
    return render(request, "main/channel_prompt.html", {"title": "Промпт для канала для GPT", "channel": channel})


def run_parser_wb_view(request):
    """Парсер Wildberries"""
    run_parser_wb()
    return render(request, 'main/index.html', {"page_obj": "Hellow World"})


def run_parser_tg_view(request):
    """Парсер Wildberries"""
    run_parser_tg()
    return render(request, 'main/index.html', {"page_obj": "Hellow World"})


def transliterate_filename(filename):
    """Транслитерирует имя файла, если оно содержит кириллицу."""
    name, ext = os.path.splitext(filename)
    if re.search('[а-яА-Я]', name):  # Проверка на кириллицу
        name = transliterate.slugify(name)  # Транслитерирует кириллицу в латиницу
    return f"{name}{ext}"


def resave(request):
    """Переименование файлов в базе данных и конвертация webp в jpg"""
    files = Media.objects.all()
    modified_files = []  # Список для отслеживания измененных файлов

    for media_file in files:
        if media_file.file:
            original_path = media_file.file.path
            original_name = os.path.basename(original_path)

            # Проверка на кириллицу в названии файла и транслитерация при необходимости
            if re.search('[а-яА-Я]', original_name):
                trans_name = transliterate_filename(original_name)
            else:
                trans_name = original_name  # Если кириллицы нет, оставляем название как есть

            # Если файл .webp, конвертируем его в .jpg
            if original_path.endswith('.webp'):
                new_name = os.path.splitext(trans_name)[0] + '.jpg'
                new_path = os.path.join(os.path.dirname(original_path), new_name)

                # Конвертация изображения в .jpg
                with Image.open(original_path) as img:
                    rgb_img = img.convert('RGB')
                    rgb_img.save(new_path, 'JPEG')

                new_path = os.path.join("media", str(media_file.post_id), new_name)
                media_file.file.name = new_path
                media_file.save()
                modified_files.append(new_name)
            elif trans_name != original_name:
                new_path = os.path.join(os.path.dirname(original_path), trans_name)
                os.rename(original_path, new_path)
                new_path = os.path.join("media", str(media_file.post_id), trans_name)
                media_file.file.name = new_path
                media_file.save()
                modified_files.append(trans_name)

    return render(request, 'main/index.html', {"page_obj": "Файлы обработаны", "modified_files": modified_files})

