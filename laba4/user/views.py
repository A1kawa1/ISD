from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import CreateView
from user.forms import CreationForm, СhangeUserForm, SelectRoleForm
from user.models import User


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('user:login')
    template_name = 'signup.html'


def home(request):
    user = request.user
    users = User.objects.all()
    if not user.is_authenticated:
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
    return render(request, 'home.html', {
        'staf': True,
        'users': users,
        'client': user
    })


@login_required
def change_info(request, id):
    user = get_object_or_404(User, id=id)
    if (request.user.role != 'vit_director'
        and request.user.role != 'director'):
        return redirect('user:home')
    form = СhangeUserForm(request.POST or None,
                      instance=user)
    if form.is_valid():
        form.save()
        return redirect('user:home')
    return render( request, 'change_info.html',{
        'form': form
    })


@login_required
def deletе_user(request, id):
    user = get_object_or_404(User, id=id)
    if request.user.role != 'director':
        return redirect('user:home')
    user.delete()
    return redirect('user:home')


@login_required
def create_user(request):
    users = User.objects.filter(role=None)
    form = SelectRoleForm(request.POST or None)
    if request.user.role != 'director':
        return redirect('user:home')
    return render(request, 'create_user.html', {
        'users': users,
        'form': form
    })



@login_required
def select_role(request, id):
    user = get_object_or_404(User, id=id)
    if request.user.role != 'director':
        return redirect('user:home')
    form = SelectRoleForm(request.POST or None)
    if form.is_valid():
        user.role = form.cleaned_data.get('role')
        user.save()
    return redirect('user:create_user')
