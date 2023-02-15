from django.contrib import admin
from user.models import User

class UserAdmin(admin.ModelAdmin):
    fields = (
        'name',
        'surename',
        'patronymic',
        'role',
        'adress',
        'phone',
        'username',
    )


admin.site.register(User, UserAdmin)
