from django.shortcuts import render
import matplotlib.pyplot as plt
import numpy as np

# Create your views here.

DATA = []


def graph(request):
    global DATA
    Y_val = request.GET.get('Y_val')
    Y_min = request.GET.get('Y_min')
    Y_max = request.GET.get('Y_max')
    fig = plt.figure()
    context = {}
    if Y_val:
        try:
            data = list(map(int, Y_val.split()))
            x = np.arange(1, len(data)+1)
            DATA = list(zip(x, data))
            plt.plot(x, data)
            plt.axhline (y=sum(data)/len(data), color='red', linestyle='--') 
            fig.savefig('static/saved_figure1.png')
            fig.clear()
            plt.bar(x, data)
            plt.axhline (y=sum(data)/len(data), color='red', linestyle='--') 
            fig.savefig('static/saved_figure2.png')
        except ValueError:
            print('Errore')
            pass
    context['data'] = [el[1] for el in DATA]
    tmp_DATA = DATA.copy()
    if Y_min:
        try:
            context['Y_min'] = int(Y_min)
            tmp_DATA = list(
                filter(lambda y_x: y_x[1] > context['Y_min'], tmp_DATA))
        except ValueError:
            Y_min = ''
    if Y_max:
        try:
            context['Y_max'] = int(Y_max)
            tmp_DATA = list(
                filter(lambda y_x: y_x[1] < context['Y_max'], tmp_DATA))
        except ValueError:
            Y_max = ''
    if Y_min or Y_max:
        print(tmp_DATA)
        plt.plot([el[0] for el in tmp_DATA], [el[1] for el in tmp_DATA])
        fig.savefig('static/saved_figure3.png')

    return render(request, 'graph.html', context)
