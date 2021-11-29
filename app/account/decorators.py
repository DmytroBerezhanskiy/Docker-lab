from django.http import HttpResponse
from django.shortcuts import redirect


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('product_list')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func


def entrepreneur_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.filter(name='entrepreneur').exists()
        if group:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('product_list')
    return wrapper_func
