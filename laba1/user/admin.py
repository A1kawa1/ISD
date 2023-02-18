from django.contrib import admin
from user.models import *


class UserAdmin(admin.ModelAdmin):
    fields = (
        'first_name',
        'last_name',
        'check_purchase',
        'curent_purchase',
        'credit_limit',
        'curend_debt',
        'lost_credit'
    )


class ProductAdmin(admin.ModelAdmin):
    fields = (
        'name',
        'count',
        'price'
    )


class OrderAdmin(admin.ModelAdmin):
    fields = (
        'user',
        'product',
        'count'
    )


admin.site.register(User, UserAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)