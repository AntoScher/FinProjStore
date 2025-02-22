from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class User(AbstractUser):
    date_birth = models.DateTimeField(blank=True, null=True, verbose_name="Дата рождения")
    #photo = models.ImageField(upload_to="users/%Y/%m/%d/", blank=True, null=True, verbose_name="Фотография")
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',  # Уникальное имя для обратного доступа
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions_set',  # Уникальное имя для обратного доступа
        blank=True,
    )






"""
"""