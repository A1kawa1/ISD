from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from user.views import (home, SignUp, change_info,
                        deletе_user, create_user, select_role)


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
    path('home/', home, name='home'),
    path(
        'change/<int:id>/',
        change_info,
        name='change_info'
    ),
    path(
        'deletе/<int:id>/',
        deletе_user,
        name='deletе_user'
    ),
    path(
        'create/',
        create_user,
        name='create_user'
    ),
    path(
        'select_role/<int:id>/',
        select_role,
        name='select_role'
    ),
]
