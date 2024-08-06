from django.contrib import admin
from django.urls import path
from .views import message_list, fetch_emails

urlpatterns = [
    path('messages/', message_list, name='message_list'),
    path('fetch-emails/', fetch_emails, name='fetch_emails'),
]
