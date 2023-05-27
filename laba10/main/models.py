from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.
class Product(models.Model):
    date = models.DateField()
    name = models.CharField(max_length=50, unique=True)
    amount = models.PositiveIntegerField()
    price = models.PositiveIntegerField(
        validators=[
            MinValueValidator(limit_value=1)
        ]
    )