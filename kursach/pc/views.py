from django.shortcuts import render
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from dataclasses import dataclass
from typing import List

from pc.forms import *
from pc.models import *


@dataclass
class Salary:
    collector: User
    total: int
    data_orders: List[AssemblyOrder]


@dataclass
class SingleOrder:
    accessories: Accessories
    percent: int
    count: int
    total: int


@dataclass
class Orders:
    group: Group
    count: int
    total: int
    list_order: List[SingleOrder]


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('pc:login')
    template_name = 'signup.html'


def home(request):
    user = request.user
    if user.is_authenticated:
        if not user.is_staff:
            orders = AssemblyOrder.objects.filter(user=user)
        else:
            orders = AssemblyOrder.objects.filter(collector=None)
        return render(
            request,
            'home.html',
            {
                'orders': orders
            }
        )
    return render(request, 'home.html')


@login_required
def add_AssemblyOrder(request):
    user = request.user
    form = CreateAssemblyOrderForm(
        request.POST or None
    )
    if form.is_valid():
        form.instance.user = user
        form.save()
        return redirect('pc:home')
    return render(
        request,
        'order.html',
        {
            'form': form
        }
    )


@login_required
def del_order(request, id):
    order = get_object_or_404(AssemblyOrder, id=id)
    if request.user != order.user:
        return redirect('pc:home')
    order.delete()
    return redirect('pc:home')


@login_required
def add_collector(request, id):
    colector = request.user
    order = get_object_or_404(AssemblyOrder, id=id)
    order.collector = colector
    order.confirmation = True
    order.save()
    return redirect('pc:home')


@login_required
def collector_orders(request):
    orders = AssemblyOrder.objects.filter(
        collector=request.user,
        assembled=False
    )
    return render(
        request,
        'collector_orders.html',
        {
            'orders': orders
        }
    )


@login_required
def set_assembled(request, id):
    total = 0
    not_null = 0

    order = get_object_or_404(AssemblyOrder, id=id)
    assembly_order_accessories = order.assembly_order_accessories.all()
    for el in assembly_order_accessories:
        print(el.accessories, el.count)
        if not el.count is None:
            not_null += 1
            total += el.count * el.accessories.price
    if len(assembly_order_accessories) == not_null:
        order.assembled = True
        order.total_price = total
        order.save()

        for el in assembly_order_accessories:
            accessories = el.accessories
            accessories.count -= el.count
            accessories.save()

    return redirect('pc:collector_orders')


@login_required
def history_orders(request):
    orders = AssemblyOrder.objects.filter(
        collector=request.user,
        assembled=True
    )
    return render(
        request,
        'history_orders.html',
        {
            'orders': orders
        }
    )


@login_required
def salary(request):
    data = []
    data_collector = (AssemblyOrder.objects
                      .filter(assembled=True)
                      .values('collector')
                      .annotate(total=Sum('total_price')))
    for el in data_collector:
        collector = get_object_or_404(User, pk=el.get('collector'))
        data_orders = AssemblyOrder.objects.filter(
            assembled=True,
            collector=collector
        )
        data.append(Salary(
            collector=collector,
            total=el.get('total'),
            data_orders=data_orders
        ))

    print(data)
    return render(
        request,
        'salary.html',
        {
            'data': data
        }
    )


@login_required
def analise_order(request):
    data = []
    data_group = (AssemblyOrderAccessories.objects
                  .filter(assembly_order__assembled=True)
                  .values('accessories__group')
                  .annotate(
                      count=Sum('count')
                  ))
    for el in data_group:
        total = 0
        group = get_object_or_404(Group, pk=el.get('accessories__group'))
        data_accessories = (AssemblyOrderAccessories.objects
                            .filter(
                                accessories__group=group
                            )
                            .values('accessories')
                            .annotate(
                                count=Sum('count')
                            ))
        for tmp in data_accessories:
            accessories = get_object_or_404(
                Accessories, pk=tmp.get('accessories'))
            tmp['percent'] = int(tmp.get('count')/el.get('count')*100)
            tmp['total'] = accessories.price*tmp.get('count')
            total += tmp['total']
            tmp['accessories'] = accessories

        res_data_accessories = [
            SingleOrder(
                accessories=tmp_el['accessories'],
                percent=tmp_el['percent'],
                count=tmp_el['count'],
                total=tmp_el['total'])
            for tmp_el in data_accessories
        ]
        data.append(
            Orders(
                group=group,
                count=el.get('count'),
                list_order=res_data_accessories,
                total=total
            )
        )
    for el in data:
        print(el)
    return render(
        request,
        'analise_order.html',
        {
            'data': data
        }
    )
