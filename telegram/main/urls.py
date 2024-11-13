from django.urls import path
from django.conf import settings

from .views import *

app_name = 'Telega_main'

urlpatterns = [
    path('', home_view, name='home'), # Главная страница
    path('tg_parser', run_parser_tg_view, name='tg_parser'), # Главная страница
    path('resave', resave, name='resave'), # Главная страница
    path('channel/<int:pk>/', get_channel_prompt, name='get_channel_prompt'),
]