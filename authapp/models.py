from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLES = (
        ('ADM', 'админ'),
        ('EMP', 'рабочий'),
        ('CLT', 'клиент')
    )
    name = models.CharField(max_length=50, blank=True)
    role = models.CharField(max_length=3, choices=ROLES, default='CLT')