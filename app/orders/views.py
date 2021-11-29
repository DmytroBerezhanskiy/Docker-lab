from django.contrib.auth.models import User
from django.shortcuts import render
from django import forms
from account.models import UserProfile
from .models import OrderItem, Order
from .forms import OrderForm
from orderlist.orderlist import OrderList


def create_order(request):
    orderlist = OrderList(request)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if orderlist.promocode:
                order.promocode = orderlist.promocode
                order.discount = orderlist.promocode.discount
            order.save()
            request.session['promocode_id'] = None
            for item in orderlist:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['count'])
            orderlist.clear()
            return render(request, 'orders/order_created.html', {'orders': order})
    else:
        if request.user.is_authenticated:
            user_prof = UserProfile.objects.get(user=request.user)
            form = OrderForm(initial={"username": request.user.username, "first_name": request.user.first_name,
                                      "last_name": request.user.last_name, "email": request.user.email,
                                      "address": user_prof.address, "telephone": user_prof.telephone})
            form.fields['username'].widget = forms.HiddenInput()
            return render(request, 'orders/order_create.html', {'orderlist': orderlist, 'form': form})
        else:
            form = OrderForm(initial={"username": "{guest}"})
            form.fields['username'].widget = forms.HiddenInput()
            return render(request, 'orders/order_create.html', {'orderlist': orderlist, 'form': form})
