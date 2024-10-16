import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'django-insecure-f7k@u72sd#+el16jww)56jqb^+@x9myqj_o+5mg32^%r5=n@o8'

DEBUG = False

ALLOWED_HOSTS = ['93.183.105.111', 'localhost', '127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'telega_db',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# STATIC_DIR = os.path.join(BASE_DIR, '/static/')
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'static'),
# ]
STATIC_ROOT = os.path.join(BASE_DIR, '/static/')
