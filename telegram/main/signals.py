from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post
from .telegram_bot import send_message_sync

@receiver(post_save, sender=Post)
def notify_telegram_on_save(sender, instance, created, **kwargs):
    """Отправляет сообщение в Telegram при создании записи"""
    if created:
        send_message_sync(f"Добавлена новая запись: {instance.name}")

