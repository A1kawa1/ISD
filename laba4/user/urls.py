from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from user.views import home, SignUp


app_name = 'user'
urlpatterns = [
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
    # path('login/', login, name='login'),
    path('home/', home, name='home')
]
