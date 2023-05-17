from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

User = get_user_model()


class Group(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=50
    )
    description = models.TextField(
        verbose_name='Описание'
    )

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self):
        return self.name


class Accessories(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=50
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    group = models.ForeignKey(
        'Group',
        related_name='accessories',
        on_delete=models.CASCADE,
        verbose_name='Группа'
    )
    price = models.PositiveIntegerField(
        verbose_name='Цена',
        validators=[
            MinValueValidator(
                limit_value=1,
                message='Минимальная цена - 1'
            )
        ]
    )
    count = models.PositiveIntegerField(
        verbose_name='Количество'
    )

    class Meta:
        verbose_name = 'Комплектующее'
        verbose_name_plural = 'Комплектующие'

    def __str__(self):
        return f'{self.group} - {self.name} {self.price}р.'


class AssemblyOrder(models.Model):
    user = models.ForeignKey(
        User,
        related_name='orders',
        on_delete=models.CASCADE,
        verbose_name='Заказчик',
        blank=True,
        null=True
    )
    name = models.CharField(
        verbose_name='Название',
        max_length=50
    )
    collector = models.ForeignKey(
        User,
        related_name='assembly_orders',
        on_delete=models.CASCADE,
        verbose_name='Сборщик',
        blank=True,
        null=True
    )
    accessories = models.ManyToManyField(
        Accessories,
        through='AssemblyOrderAccessories',
        verbose_name='Комплектующие'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now=True
    )
    confirmation = models.BooleanField(default=False)
    assembled = models.BooleanField(default=False)
    total_price = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Наряд на сборку'
        verbose_name_plural = 'Наряды на сборку'
        ordering = ('-pub_date',)


class AssemblyOrderAccessories(models.Model):
    assembly_order = models.ForeignKey(
        AssemblyOrder,
        on_delete=models.CASCADE,
        verbose_name='Наряд на сборку'
    )
    accessories = models.ForeignKey(
        Accessories,
        on_delete=models.CASCADE,
        verbose_name='Комплектующее'
    )
    count = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        validators=[
            MinValueValidator(
                limit_value=1,
                message='Минимальное количество - 1'
            )
        ],
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Комплектующее - Наряд на сборку'
        verbose_name_plural = 'Комплектующие - Наряды на сборку'
        default_related_name = 'assembly_order_accessories'

    def clean(self) -> None:
        count = self.accessories.count
        if not self.count is None and count < self.count:
            raise ValidationError(f'Доступно {count}')


class ShoppingList(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    accessories = models.ForeignKey(
        Accessories,
        on_delete=models.CASCADE,
        verbose_name='Комплектующее'
    )
    count = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        validators=[
            MinValueValidator(
                limit_value=1,
                message='Минимальное количество - 1'
            )
        ],
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'
        default_related_name = 'shopping_list'

    def clean(self) -> None:
        count = self.accessories.count
        if not self.count is None and count < self.count:
            raise ValidationError(f'Доступно {count}')
