from .orderlist import OrderList


def orderlist(request):
    return {'orderlist': OrderList(request)}
