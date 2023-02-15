from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


User = get_user_model()


class CreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('name', 'surename', 'patronymic', 'username')
