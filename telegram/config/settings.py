from pathlib import Path
import os

try:
    from .local_settings import *
except ImportError:
    from .prod_settings import *

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    "main.apps.MainConfig",

    "ckeditor"
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

STATIC_URL = '/staticfiles/'

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Asia/Yekaterinburg'

USE_I18N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000

CKEDITOR_CONFIGS = {
    'default': {
        'width': 650,  # Ширина редактора
        'height': 300,  # Высота редактора
        'toolbar': [
            ['Spoiler', 'Blockquote', '-', 'Bold', 'Italic', 'Underline', 'Link', "Unlink"],
            ['Undo', 'Redo'],
            ['Source'],
        ],
        'extraPlugins': 'spoiler, blockquote',  # Подключаем плагин
        'autoParagraph': False,  # Отключаем автоматическое оборачивание текста в <p>
        'allowedContent': True,  # Разрешаем любые данные
        'fillEmptyBlocks': False,
        'extraAllowedContent': 'spoiler',  # Явно разрешаем тег <spoiler>
        'enterMode': 2,  # Отключаем стандартное поведение Enter
        'shiftEnterMode': 3,  # Отключаем Shift+Enter
    }
}