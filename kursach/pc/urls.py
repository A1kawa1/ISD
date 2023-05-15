from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from pc.views import *


app_name = 'pc'
urlpatterns = [
    path('', home, name='home'),
    path(
        'login/',
        LoginView.as_view(template_name='login.html'),
        name='login'
    ),
    path(
        'logout/',
        LogoutView.as_view(template_name='logged_out.html'),
        name='logout'
    ),
    path(
        'signup/',
        SignUp.as_view(),
        name='signup'
    ),
    path(
        'order/',
        add_AssemblyOrder,
        name='add_AssemblyOrder'
    ),
    path(
        'del_order/<int:id>/',
        del_order,
        name='del_order'
    ),
    path(
        'add_collector/<int:id>/',
        add_collector,
        name='add_collector'
    ),
    path(
        'collector_orders/',
        collector_orders,
        name='collector_orders'
    ),
    path(
        'set_assembled/<int:id>/',
        set_assembled,
        name='set_assembled'
    ),
    path(
        'history_orders/',
        history_orders,
        name='history_orders'
    ),
    path(
        'salary/',
        salary,
        name='salary'
    ),
    path(
        'analise_order/',
        analise_order,
        name='analise_order'
    )
    # path(
    #     'configure_accessories/<int:id>/',
    #     configure_accessories,
    #     name='configure_accessories'
    # ),
    # path(
    #     'add_accessories/<int:id>/',
    #     add_accessories,
    #     name='add_accessories'
    # )
]
