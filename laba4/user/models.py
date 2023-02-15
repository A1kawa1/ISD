from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('secretary', 'secretary'),
        ('vit_director', 'vit_director'),
        ('director', 'director'),
    )

    name = models.CharField(verbose_name='Имя', max_length=50)
    surename = models.CharField(verbose_name='Фамилия', max_length=50)
    patronymic = models.CharField(verbose_name='Отчество', max_length=50, blank=True)
    role = models.CharField(
        verbose_name='role',
        max_length=255,
        choices=ROLE_CHOICES,
        blank=True,
        null=True,
    )
    adress = models.CharField(verbose_name='Адрес', max_length=100, blank=True)
    phone = models.CharField(verbose_name='Телефон', max_length=11, blank=True)

    @property
    def is_secretary(self):
        return self.role == 'secretary'

    @property
    def is_vit_director(self):
        return self.role == 'vit_director'
