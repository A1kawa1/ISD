from django.shortcuts import render
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F
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


@dataclass
class SingleCheque:
    accessories: Accessories
    price: int
    count: int
    total: int


@dataclass
class AccessoriesHome:
    accessories: Accessories
    add_shop_list: bool


@dataclass
class CollectorOrders:
    orders: AssemblyOrder
    set_assembled: bool


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('pc:login')
    template_name = 'signup.html'


def home(request):
    user = request.user
    if user.is_authenticated:
        if not user.is_staff:
            data = []
            accessories = Accessories.objects.all()
            for el in accessories:
                shop_accessories = ShoppingList.objects.filter(
                    user=user,
                    accessories=el
                ).exists()
                data.append(
                    AccessoriesHome(
                        accessories=el,
                        add_shop_list=not shop_accessories
                    )
                )
            context = {
                'data': data
            }
        else:
            orders = AssemblyOrder.objects.filter(collector=None)
            context = {
                'orders': orders
            }
        return render(
            request,
            'home.html',
            context
        )
    return render(request, 'home.html')


@login_required
def add_shoppinglist(request, id):
    user = request.user
    accessories = get_object_or_404(Accessories, pk=id)
    shop, create = ShoppingList.objects.get_or_create(
        user=user,
        accessories=accessories
    )
    if create:
        shop.count = 1
    else:
        shop.count += 1
    shop.save()
    return redirect('pc:home')


@login_required
def basket(request):
    total_price = 0
    user = request.user
    user_basket = ShoppingList.objects.filter(user=user)
    total = user_basket.values('accessories').annotate(
        summ=F('count')*F('accessories__price'))
    for el in total:
        total_price += el.get('summ')
    return render(
        request,
        'basket.html',
        {
            'user_basket': user_basket,
            'total_price': total_price
        }
    )


@login_required
def plus_count(request, id):
    user = request.user
    accessories = get_object_or_404(Accessories, pk=id)
    shop, create = ShoppingList.objects.get_or_create(
        user=user,
        accessories=accessories
    )
    if create:
        shop.count = 1
    else:
        shop.count += 1
    shop.save()
    return redirect('pc:basket')


@login_required
def minus_count(request, id):
    user = request.user
    accessories = get_object_or_404(Accessories, pk=id)
    shop = get_object_or_404(
        ShoppingList,
        user=user,
        accessories=accessories
    )

    shop.count -= 1
    shop.save()
    if shop.count == 0:
        shop.delete()
    return redirect('pc:basket')


@login_required
def del_shop_item(request, id):
    shop = get_object_or_404(ShoppingList, id=id)
    shop.delete()
    return redirect('pc:basket')


@login_required
def add_order(request):
    total_price = 0
    user = request.user
    shopping_list = ShoppingList.objects.filter(user=user)

    total = shopping_list.values('accessories').annotate(
        summ=F('count')*F('accessories__price'))

    for el in total:
        total_price += el.get('summ')

    print(shopping_list)
    assembly_order = AssemblyOrder.objects.create(
        user=user,
        name='None',
        total_price=total_price
    )
    assembly_order.name = f'№{assembly_order.pk}'
    assembly_order.save()

    for el in shopping_list:
        AssemblyOrderAccessories.objects.create(
            assembly_order=assembly_order,
            accessories=el.accessories,
            count=el.count
        )
    shopping_list.delete()
    return redirect('pc:basket')


@login_required
def user_order(request):
    user = request.user
    orders = AssemblyOrder.objects.filter(user=user)
    return render(
        request,
        'user_order.html',
        {
            'orders': orders
        }
    )


@login_required
def view_cheque(request, id):
    total_price = 0
    res_data = []
    user = request.user
    orders = get_object_or_404(
        AssemblyOrder,
        user=user,
        id=id
    )
    assembly_order_accessories = AssemblyOrderAccessories.objects.filter(
        assembly_order=orders)
    data = (assembly_order_accessories
            .values('accessories')
            .annotate(
                price=F('accessories__price'),
                count=F('count'),
                total=F('count')*F('accessories__price')
            ))
    print(data)
    for el in data:
        res_data.append(SingleCheque(
            accessories=get_object_or_404(
                Accessories, pk=el.get('accessories')),
            price=el.get('price'),
            count=el.get('count'),
            total=el.get('total'),
        ))
        total_price += el.get('total')

    return render(
        request,
        'view_cheque.html',
        {
            'data': res_data,
            'total_price': total_price
        }
    )


@ login_required
def add_collector(request, id):
    colector = request.user
    order = get_object_or_404(AssemblyOrder, id=id)
    order.collector = colector
    order.confirmation = True
    order.save()
    return redirect('pc:home')


@ login_required
def collector_orders(request):
    data = []
    orders = AssemblyOrder.objects.filter(
        collector=request.user,
        assembled=False
    )
    for el in orders:
        assembly_order_accessories = el.assembly_order_accessories.all()
        flag_set_assembled = True
        for accessories in assembly_order_accessories:
            if accessories.count > accessories.accessories.count:
                flag_set_assembled = False
        print(flag_set_assembled)
        data.append(
            CollectorOrders(
                orders=el,
                set_assembled=flag_set_assembled
            )
        )
    return render(
        request,
        'collector_orders.html',
        {
            'orders': data
        }
    )


@ login_required
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


@ login_required
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


@ login_required
def salary(request):
    data = []
    data_collector = set((AssemblyOrder.objects
                          .filter(assembled=True)
                          .values_list('collector', flat=True)
                          .distinct()))

    for pk in data_collector:
        collector = get_object_or_404(User, pk=pk)
        data_orders = AssemblyOrder.objects.filter(
            assembled=True,
            collector=collector
        )
        total = data_orders.aggregate(
            total=Sum('total_price')).get('total')*0.03
        data.append(Salary(
            collector=collector,
            total=int(total),
            data_orders=data_orders
        ))

    for el in data:
        print(el)
    return render(
        request,
        'salary.html',
        {
            'data': data
        }
    )


@ login_required
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
                                accessories__group=group,
                                assembly_order__assembled=True
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
