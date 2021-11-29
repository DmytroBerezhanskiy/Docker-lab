from django.urls import path
from . import views

app_name = 'orderlist'

urlpatterns = [
    path('', views.orderlist_detail, name='orderlist_detail'),
    path('add/<int:product_id>/', views.orderlist_add, name='orderlist_add'),
    path('delete/<int:product_id>/', views.orderlist_delete, name='orderlist_delete'),
]
