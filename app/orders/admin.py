from django.contrib import admin

from orders.models import Order, OrderItem


class OrderInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


@admin.register(Order)
class OrderAdminModel(admin.ModelAdmin):
    list_display = ['id', 'username', 'first_name', 'last_name', 'email', 'telephone', 'address', 'courier', 'status', 'note', 'paid', 'created', 'updated']
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderInline]


