from django.shortcuts import render
from main.forms import DateForm
import datetime

from main.models import Product

# Create your views here.
def main(request):
    form = DateForm(request.POST or None)
    products = Product.objects.all()

    if request.method == 'POST':
        date = form.data.get('date')
        if date == '':
            return render(request, 'home.html', {
                'form':form,
                'products': products
            })
        date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        products = products.filter(date__lte=date)
        return render(request, 'home.html', {
            'form':form,
            'products': products
        })
    return render(request, 'home.html', {
        'form':form,
        'products': products
    })