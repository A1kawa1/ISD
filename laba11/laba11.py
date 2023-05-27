import matplotlib.pyplot as plt
import numpy as np
from math import sqrt


def f(x):
    return 1 / x


def F(functions, x):
    functions = functions[::-1]
    tmp = x
    for func in functions:
        tmp = func(tmp)
    return tmp


fun = {
    '1': ('sqrt(x)', sqrt),
    '2': ('1/x', f),
    '3': ('np.exp(x)', np.exp)
}


for i, fu in fun.items():
    print(f'{i} - {fu[0]}')

inp = input('Введите набор функций: ')
data_fun = [fun.get(el)[1] for el in inp]

odz = map(float, input('Введите промежуток: ').split())
a, b = odz
x_data = np.linspace(a, b, 100)

x_res, y_rez = [], []
for x in x_data:
    try:
        y_rez.append(F(data_fun, x))
        x_res.append(x)
    except:
        ...

plt.plot(x_res, y_rez)
plt.show()
