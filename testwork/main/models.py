from django.db import models

from django.db import models

class Message(models.Model):
    subject = models.CharField(max_length=100, verbose_name='Тема сообщения')
    date_sent = models.DateTimeField(verbose_name='Дата отправки')
    date_received = models.DateTimeField(verbose_name='Дата получения')
    message_text = models.TextField(verbose_name='Описание или текст сообщения')

    def __str__(self):
        return self.subject

class Attachment(models.Model):
    message = models.ForeignKey(Message, related_name='attachments', on_delete=models.CASCADE)
    file = models.FileField(upload_to='attachments/', verbose_name='Файл')

    def __str__(self):
        return self.file.name
