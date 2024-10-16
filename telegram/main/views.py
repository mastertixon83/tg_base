from django.shortcuts import render
from utils.parser_wb.parser import run_parser_wb, run_parser_tg


def home_view(request):
    """Вывод главной стрницы"""
    # Возвращаем объекты страницы вместе с пагинатором в контексте
    return render(request, 'main/index.html', {"page_obj": "Hellow World"})


def run_parser_wb_view(request):
    """Парсер Wildberries"""
    run_parser_wb()
    return render(request, 'main/index.html', {"page_obj": "Hellow World"})


def run_parser_tg_view(request):
    """Парсер Wildberries"""
    run_parser_tg()
    return render(request, 'main/index.html', {"page_obj": "Hellow World"})
