from django.urls import path
from . import views

urlpatterns = [
    path('menu/', views.menu, name='main_menu'),
    path('menu/<int:pk>', views.menu_li, name='menu'),
]