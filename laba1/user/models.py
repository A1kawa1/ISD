from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import AbstractUser


class Product(models.Model):
    name = models.CharField(max_length=50)
    count = models.IntegerField(
        validators=[
            MinValueValidator(0)
        ]
    )
    price = models.IntegerField(
        validators=[
            MinValueValidator(0)
        ]
    )

    def __str__(self):
        return self.name


class User(AbstractUser):
    check_purchase = models.IntegerField(
        default=0,
        validators=[
            MinValueValidator(0)
        ]
    )   
    curent_purchase = models.IntegerField(
        default=5000,
        validators=[
            MinValueValidator(0)
        ]
    )
    credit_limit = models.IntegerField(
        default=2000
    )
    curend_debt = models.IntegerField(
        default=0
    )
    lost_credit = models.IntegerField(
        default=2000
    )
    comment = models.TextField()


class Order(models.Model):
    CHOIES = (
        ('cash', 'наличный расчет'),
        ('card', 'безналичный расчет'),
        ('credit', 'кредит'),
        ('barter', 'бартер')
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='order'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    count = models.IntegerField(
        validators=[
            MinValueValidator(0)
        ]
    )
    type = models.CharField(
        choices=CHOIES,
        max_length=50,
        default=None
    )
    price = models.IntegerField(
        validators=[
            MinValueValidator(0)
        ]
    )
