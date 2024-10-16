command = '/mnt/96375fe5-6a39-4e72-b221-433152ae3028/u4eba/Python/bots/telega/telega_main/venv/bin/gunicorn'
pythonpath = '/mnt/96375fe5-6a39-4e72-b221-433152ae3028/u4eba/Python/bots/telega/telega_main/telegram'
bind = '0.0.0.0:8000'

#количество воркеров 2*кол-во ядер процессора + 1
workers = 3
user = 'tixon'
limit_request_fields = 32000
limit_request_field_size = 0
raw_env = 'DJANGO_SETTINGS_MODULE=config.settings'
