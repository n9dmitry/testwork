from django.shortcuts import render
from .models import Menu

def menu(request):
    menus = Menu.objects.all()

    # menu = [
    #     {"title": "Главная", "url": "/"},
    #     {"title": "Новости", "url": "/news", "sublinks": [
    #         {"title": "Новость 1", "url": "/news/1"},
    #         {"title": "Новость 2", "url": "/news/2"}
    #     ]},
    #     {"title": "Контакты", "url": "/contacts"}
    # ]
    print(menus)

def menu_li(request):
    pass
