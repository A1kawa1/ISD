from django.contrib.admin import ModelAdmin, TabularInline, register
from pc.models import *


@register(Group)
class GroupAdmin(ModelAdmin):
    list_display = ('name', 'description')


@register(Accessories)
class AccessoriesAdmin(ModelAdmin):
    list_display = ('name', 'description', 'group', 'count', 'price')


class AccessoriesInline(TabularInline):
    model = AssemblyOrderAccessories
    extra = 1


@register(AssemblyOrder)
class AssemblyOrderAdmin(ModelAdmin):
    list_display = ('name', 'collector', 'pub_date',
                    'confirmation', 'assembled')
    inlines = (AccessoriesInline,)
