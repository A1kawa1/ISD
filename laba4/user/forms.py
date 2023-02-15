from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms


User = get_user_model()


class CreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('name', 'surename', 'patronymic', 'username')


class СhangeUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'name',
            'surename',
            'patronymic',
            'role',
            'adress',
            'phone',
        )


class SelectRoleForm(forms.Form):
    ROLE_CHOICES = (
        ('secretary', 'secretary'),
        ('vit_director', 'vit_director'),
        ('director', 'director'),
    )
    role = forms.ChoiceField(choices=ROLE_CHOICES)
