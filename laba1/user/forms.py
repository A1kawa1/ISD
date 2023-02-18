from django import forms
from django.contrib.auth.forms import UserCreationForm
from user.models import Order, User


class CreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username'
        )


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            'product',
            'count',
            'type'
        )

    def clean_count(self):
        count = self.cleaned_data['product'].count
        if count < self.cleaned_data['count']:
            raise forms.ValidationError(
                f'Простите, но выберите меньшее кол-во товаров. Доступно {count}'
            )
        return self.cleaned_data['count']
