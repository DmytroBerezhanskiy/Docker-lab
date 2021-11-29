from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from promocode.forms import PromocodeForm
from .forms import OrderListAddProductForm
from .orderlist import OrderList
from shop.models import Product


@require_POST
def orderlist_add(request, product_id):
    orderlist = OrderList(request)
    product = Product.objects.get(id=product_id)
    form = OrderListAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        orderlist.add(product=product,
                      count=cd['count'],
                      update_count=cd['update'])
    return redirect('orderlist:orderlist_detail')


def orderlist_delete(request, product_id):
    ordelist = OrderList(request)
    product = Product.objects.get(id=product_id)
    ordelist.delete(product)
    return redirect('orderlist:orderlist_detail')


def orderlist_detail(request):
    orderlist = OrderList(request)
    for item in orderlist:
        item['update_count'] = OrderListAddProductForm(
                            initial={'count': item['count'],
                                     'update': True})
    form = PromocodeForm()
    return render(request, 'orderlist/detail.html', {'orderlist': orderlist, "form": form})
