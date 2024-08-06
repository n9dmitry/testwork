from django.contrib import admin

from .models import Message, Attachment


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'date_sent', 'date_received')  # Поля, которые будут отображаться в списке
    search_fields = ('subject', 'message_text')  # Поля для поиска
    list_filter = ('date_sent', 'date_received')  # Фильтры для боковой панели


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ('message', 'file')  # Поля, которые будут отображаться в списке
    search_fields = ('file',)  # Поля для поиска
    list_filter = ('message',)  # Фильтры для боковой панели
