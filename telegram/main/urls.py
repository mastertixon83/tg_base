from django.urls import path
from django.conf import settings

from .views import *

app_name = 'Telega_main'

urlpatterns = [
    path('', home_view, name='home'), # Главная страница
    path('channel/<int:pk>/', get_channel_prompt, name='get_channel_prompt'),
]