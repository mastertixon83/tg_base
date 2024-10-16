from django.contrib import admin
from django.utils.safestring import mark_safe
from django.urls import reverse
from django import forms

from .models import *

try:
    admin.site.unregister(Channel)
except admin.sites.NotRegistered:
    pass


class ButtonInline(admin.TabularInline):
    """Инлайн-класс для отображения медиафайлов для постов"""
    model = Button
    extra = 1  # Количество пустых медиафайлов для добавления

    fields = ['text', 'link']


class MediaInline(admin.TabularInline):
    """Инлайн-класс для отображения медиафайлов для постов"""
    model = Media
    extra = 1  # Количество пустых медиафайлов для добавления

    fields = ['file', "spoiler", 'preview']
    readonly_fields = ['preview']

    def preview(self, obj):
        if obj.file:
            return mark_safe(f'<img src="{obj.file.url}" style="width: 100px; height: auto;" />')
        return ""

    preview.short_description = 'Превью'


class PostAdminForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        widgets = {
            'text': forms.Textarea(attrs={'style': 'width: 400px; height: 200px'}),
        }


class PostInline(admin.TabularInline):
    """Инлайн-класс для отображения постов в таблице на странице канала"""
    model = Post
    form = PostAdminForm
    extra = 1  # Количество пустых постов для добавления
    fields = ["post_data", "post_time", "status", "post_type", "text", "edit_link"]
    readonly_fields = ["created_at", "updated_at", "edit_link"]
    ordering = ["post_data", "post_time"]
    inlines = [MediaInline, ButtonInline]  # Добавляем инлайн для медиафайлов

    def edit_link(self, obj):
        if obj.pk:  # Проверяем, что объект уже сохранен (существует в базе)
            # Замените 'yourapp' на фактическое имя приложения
            url = reverse('admin:main_post_change', args=[obj.pk])
            return mark_safe(f'<a href="{url}" target="_blank">Edit Post</a>')
        return "Save to edit"

    edit_link.short_description = 'Edit Link'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Класс регистрации модели Категории"""
    save_on_top = True
    save_as = True
    save_as_continue = True
    search_fields = ["category"]

    list_display = ["pk", "category"]
    list_display_links = ["pk", "category"]
    list_filter = ["category"]
    ordering = ["category"]


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    """Класс регистрации модели канала"""
    save_on_top = True
    save_as = True
    save_as_continue = True
    search_fields = ["title"]
    inlines = [PostInline]

    list_display = ["pk", "title", "url", "category", "admin", "created_at"]
    list_display_links = ["pk", "title", "url"]
    list_filter = ["title"]
    ordering = ["title"]


@admin.register(Button)
class ButtonAdmin(admin.ModelAdmin):
    """Класс регистрации модели внопок"""
    save_on_top = True
    save_as = True
    save_as_continue = True

    list_display = ("pk", "text", "link", 'post__id')  # Добавляем кастомное поле с ID и текстом поста
    search_fields = ('text', 'post__text')

    list_display_links = ["pk", "text", "link"]


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Класс регистрации модели поста"""
    save_on_top = True
    save_as = True
    save_as_continue = True
    search_fields = ["text"]

    list_display = ["pk", "post_data", "post_time", "status", "ads_status", "post_type", "text", "comment", "channel", "message_id"]
    list_display_links = ["pk", "post_data", "post_time", "text"]
    list_filter = ["channel__title", "post_time", "status", "product_category"]
    list_editable = ["status", "post_type"]
    ordering = ["created_at"]
    inlines = [MediaInline, ButtonInline]


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    """Класс регистрации модели медиафайлов"""
    save_on_top = True
    save_as = True
    save_as_continue = True
    search_fields = ["file"]

    list_display = ["pk", "file", "spoiler", "preview"]
    list_display_links = ["pk", "file"]
    list_filter = ["post__text"]
    ordering = ["created_at"]


@admin.register(Admin)
class AdminsAdmin(admin.ModelAdmin):
    """Класс регистрации модели админы"""
    save_on_top = True
    save_as = True
    save_as_continue = True
    search_fields = ["nickname", "name"]

    list_display = ["pk", "nickname", "name"]
    list_display_links = ["pk", "nickname"]
    list_filter = ["nickname", "name"]
    ordering = ["nickname"]


@admin.register(BotToken)
class TokensAdmin(admin.ModelAdmin):
    """Класс регистрации модели админы"""
    save_on_top = True
    save_as = True
    save_as_continue = True
    search_fields = ["token", "name", "channel", "chat_id"]

    list_display = ["pk", "token", "name", "channel", "chat_id"]
    list_display_links = ["pk", "token"]
    list_filter = ["token", "name"]
    ordering = ["name"]
