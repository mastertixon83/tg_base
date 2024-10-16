command = '/home/tixon/telegram/tg_base/venv/bin/gunicorn'
pythonpath = '/home/tixon/telegram/tg_base/telegram'
bind = '127.0.0.1:8000'

#количество воркеров 2*кол-во ядер процессора + 1
workers = 2
user = 'tixon'
limit_request_fields = 32000
limit_request_field_size = 0
raw_env = 'DJANGO_SETTINGS_MODULE=telegram.config.settings'
