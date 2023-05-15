from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from pc.models import AssemblyOrder, Accessories

User = get_user_model()


class CreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username'
        )


class CreateAssemblyOrderForm(forms.ModelForm):
    class Meta:
        model = AssemblyOrder
        fields = ('name', 'accessories')

    accessories = forms.ModelMultipleChoiceField(
        queryset=Accessories.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label='Комплектующие'
    )
