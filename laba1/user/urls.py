from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from user.views import (SignUp, home, order, product, del_order, client,
                        edit_product, add_product, order_for_manager, barter)


app_name = 'user'
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
    path('order/', order, name='order'),
    path('del_order/<int:id>/', del_order, name='del_order'),
    path('client/', client, name='client'),
    path('product/', product, name='product'),
    path('edit_product/<int:id>/', edit_product, name='edit_product'),
    path('add_product/', add_product, name='add_product'),
    path('order_for_manager/', order_for_manager, name='order_for_manager'),
    path('barter/', barter, name='barter')
]
