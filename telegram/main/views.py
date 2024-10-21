from django.shortcuts import render
from utils.parser_wb.parser import run_parser_wb, run_parser_tg
from .models import Channel


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
