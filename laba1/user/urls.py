from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from user.views import SignUp, home, order


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
    path('order/', order, name='order')
]
