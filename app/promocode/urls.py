from django.urls import path
from . import views

urlpatterns = [
    path('apply/', views.promocode_apply, name='promocode_apply'),
]