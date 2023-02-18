from django import forms
from django.contrib.auth.forms import UserCreationForm
from user.models import Order, User, Product


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


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = (
            'name',
            'count',
            'price'
        )


class BarterForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            'product',
            'count',
            'type',
            'product2',
            'count2',
        )

    def clean(self):
        data = self.cleaned_data
        price1 = data['product'].price * data['count']
        price2 = data['product2'].price * data['count2']
        if price2 < price1:
            raise forms.ValidationError(
                f'Простите, но выберите другие товары. Не хватает {price1 - price2}р.'
            )
