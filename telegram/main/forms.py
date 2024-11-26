from django import forms
from .models import Post


class CustomEditorForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "post_type",
            'text',
            "answers",
            "comment",
            "article",
            "channel",
            "post_data",
            "post_time",
            "status",
            "date_time_publication",
            "message_id",
            "ads_status",
            "product_category"
        ]  # Поле, которое нужно редактировать
        widgets = {
            'text': forms.Textarea(attrs={'id': 'editor'}),  # ID для Textarea
        }

    class Media:
        js = ('custom_editor.js', 'answers.js')  # Подключаем кастомный JS
        css = {
            'all': ('custom_editor.css',),  # Подключаем кастомный CSS
        }

