from django import forms
from .models import Post  # Замените на вашу модель


class CustomEditorForm(forms.ModelForm):
    class Meta:
        model = Post  # Ваша модель
        fields = [
            'text',
            "comment",
            "article",
            "channel",
            "post_data",
            "post_time",
            "status",
            "date_time_publication",
            "post_type",
            "options",
            "message_id",
            "ads_status",
            "product_category"
        ]  # Поле, которое нужно редактировать
        widgets = {
            'text': forms.Textarea(attrs={'id': 'editor'}),  # ID для Textarea
        }

    class Media:
        js = ('custom_editor.js',)  # Подключаем кастомный JS
        css = {
            'all': ('custom_editor.css',),  # Подключаем кастомный CSS
        }

