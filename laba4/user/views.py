from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import CreateView
from user.forms import CreationForm
from user.models import User


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('user:login')
    template_name = 'signup.html'


def home(request):
    user = request.user
    users = User.objects.all()
    if not user.is_authenticated:
        print('user')
        context = {
            'staf': False,
            'user': True,
            'users': users
        }
        return render(request, 'home.html', context)
    if user.role is None:
        print('role None')
        return render(request, 'home.html', {
            'staf': False,
            'user': False
        })
    print('staf')
    print(user.username)
    return render(request, 'home.html', {
        'staf': True,
        'users': users
    })
