from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.urls import reverse_lazy
from user.forms import OrderForm, CreationForm, ProductForm, BarterForm
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
        form.instance.user = user
        data = form.data
        if data.get('type') == 'бартер':
            form.save()
            return redirect('user:barter')
        product = Product.objects.get(id=int(data.get('product')))
        price = product.price * int(data.get('count'))

        if (data.get('type') == 'безналичный расчет'
            and user.curent_purchase < price):
            form.add_error('type', 'У вас недостаточно средств для этого типа')
            return render(request, 'order.html', {
                'form': form
            })
        if data.get('type') == 'наличный расчет':
            user.check_purchase += price
        if data.get('type') == 'безналичный расчет':
            user.check_purchase += price
            user.curent_purchase -= price
        if data.get('type') == 'кредит':
            if user.lost_credit + user.curent_purchase < price:
                form.add_error('type', 'У вас недостаточно средств для этого типа')
                return render(request, 'order.html', {
                    'form': form
                })
            if user.curent_purchase >= price:
                user.check_purchase += price
                user.curent_purchase -= price
            else:
                user.check_purchase += price
                user.curend_debt += price - user.curent_purchase
                user.curent_purchase = 0
                user.save()
                user.lost_credit = user.credit_limit - user.curend_debt
        product.count -= int(data.get('count'))
        form.instance.price = price
        user.save()
        product.save()
        form.save()
        return redirect('user:home')
    return render(request, 'order.html', {
        'form': form
    })


@login_required
def del_order(request, id):
    order = get_object_or_404(Order, id=id)
    if request.user != order.user:
        return redirect('user:home')
    order.delete()
    return redirect('user:home')


@login_required
def barter(request):
    order = Order.objects.filter(user=request.user, type='бартер').last()
    form = BarterForm(request.POST or None,
                      instance=order)
    if form.is_valid():
        data = form.data
        product = Product.objects.get(id=int(data.get('product')))
        product.count -= int(data.get('count'))
        product2 = Product.objects.get(id=int(data.get('product2')))
        product2.count += int(data.get('count2'))
        product.save()
        product2.save()
        form.save()
        return redirect('user:home')
    return render(request, 'barter.html', {
        'form': form
    })


@login_required
def product(request):
    if not request.user.is_staff:
        return redirect('user:home')
    products = Product.objects.all()[::-1]
    return render(request, 'product.html', {
        'products': products
    })


@login_required
def edit_product(request, id):
    if not request.user.is_staff:
        return redirect('user:home')
    product = Product.objects.get(id=id)
    form = ProductForm(request.POST or None,
                       instance=product)
    if form.is_valid():
        form.save()
        return redirect('user:product')
    return render(request, 'edit_product.html', {
        'form': form
    })


@login_required
def add_product(request):
    if not request.user.is_staff:
        return redirect('user:home')
    form = ProductForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('user:product')
    return render(request, 'edit_product.html', {
        'form': form
    })


@login_required
def order_for_manager(request):
    if not request.user.is_staff:
        return redirect('user:home')
    search = request.GET.get('search', '')
    if search:
        orders = Order.objects.filter(user__last_name__icontains=search)
    else:
        orders = Order.objects.all()
    return render(request, 'order_for_manager.html', {
        'orders': orders
    })


@login_required
def client(request):
    if not request.user.is_staff:
        return redirect('user:home')
    search = request.GET.get('search', '')
    if search:
        client = User.objects.filter(Q(last_name__icontains=search) & Q(is_staff=0))
    else:
        client = User.objects.filter(is_staff=0)
    return render(request, 'client.html', {
        'client': client
    })
