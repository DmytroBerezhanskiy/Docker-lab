from django.contrib import admin
from .models import Promocode


@admin.register(Promocode)
class PromocodeAdminModel(admin.ModelAdmin):
    list_display = ('code', 'actual_from', 'actual_to', 'discount', 'active')
    ordering = ('code',)
