from django.contrib import admin
from .models import Menu


class Menu(admin.ModelAdmin):
    list_display = ('title',)  # Отображение поля title в списке


admin.site.register(Menu)