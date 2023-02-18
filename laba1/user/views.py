from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.urls import reverse_lazy
from user.forms import OrderForm, CreationForm
from user.models import *


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('user:login')
    template_name = 'signup.html'


def home(request):
    if request.user.is_authenticated:
        user = request.user
        orders = Order.objects.filter(user=user)[::-1]
        return render(request, 'home.html', {
            'orders': orders
        })
    return render(request, 'home.html')


@login_required
def order(request):
    user = request.user
    form = OrderForm(request.POST or None)
    if form.is_valid():
        data = form.data
        product = Product.objects.get(id=int(data.get('product')))
        product.count -= int(data.get('count'))

        form.instance.user = user
        form.instance.price = product.price * int(data.get('count'))
        product.save()
        form.save()
        return redirect('user:home')
    return render(request, 'order.html', {
        'form': form
    })