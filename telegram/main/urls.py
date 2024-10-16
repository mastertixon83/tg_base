from django.urls import path
from django.conf import settings

from .views import *

app_name = 'Telega_main'

urlpatterns = [
    path('', home_view, name='home'), # Главная страница
    path("parserwb", run_parser_wb_view, name="parserwb"),
    path("parsertg", run_parser_tg_view, name="parsertg")
]
