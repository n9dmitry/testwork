from django.db import models

class Menu(models.Model):
    title = models.CharField(max_length=100)
    parent_id = models.CharField(max_length=100)


# Главная
    # 1
    # 2
    # 3
# Новости
    # 1
    # 2
    # 3
# Контакты
    # 1
    # 2
    # 3