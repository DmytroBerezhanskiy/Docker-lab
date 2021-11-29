from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login

from courier.forms import CouriersReviewForm
from orders.models import Order, OrderItem
from .forms import RegistrationForm, UserEditForm, ProfileEditForm, CreateProductForm, LoginForm, \
    ShopRegistrationForm, CreateCategoryForm
from .models import UserProfile
from shop.models import Product, Shop
from .decorators import unauthenticated_user, entrepreneur_only


@unauthenticated_user
def register(request):
    if request.method == 'POST':
        register_form = RegistrationForm(request.POST)
        shop_form = ShopRegistrationForm(request.POST)
        if register_form.is_valid():
            new_user = register_form.save(commit=False)
            new_user.set_password(register_form.cleaned_data['password'])
            new_user.save()
            if shop_form.is_valid():
                if shop_form.cleaned_data['name']:
                    new_shop = shop_form.save(commit=False)
                    Shop.objects.create(owner=new_user, name=new_shop)
            UserProfile.objects.create(user=new_user)
            group = Group.objects.get(name=register_form.cleaned_data['register_like'])
            new_user.groups.add(group)
            return render(request, 'registration/register_done.html', {'new_user': new_user})
    else:
        register_form = RegistrationForm()
        shop_form = ShopRegistrationForm()
    return render(request, 'registration/register.html', {'register_form': register_form,
                                                          'shop_form': shop_form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.userprofile, data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully')
        else:
            messages.error(request, 'Something\'s going wrong')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.userprofile)
    return render(request, 'registration/edit.html', {'user_form': user_form, 'profile_form': profile_form})


@login_required
@entrepreneur_only
def createProduct(request):
    shop = Shop.objects.get(owner=request.user)
    form = CreateProductForm(initial={'shop': shop})
    form.fields['shop'].widget = forms.HiddenInput()
    if request.method == "POST":
        form = CreateProductForm(request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('my_products')
    context = {'form': form}
    return render(request, 'registration/CRUD/create_product.html', context)


@login_required
@entrepreneur_only
def updateProduct(request, id, slug):
    product = Product.objects.get(id=id, slug=slug)
    form = CreateProductForm(instance=product)
    form.fields['shop'].widget = forms.HiddenInput()
    if request.method == 'POST':
        form = CreateProductForm(request.POST, instance=product, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('my_products')
    context = {"form": form}
    return render(request, 'registration/CRUD/update_product.html', context)


@login_required
@entrepreneur_only
def deleteProduct(request, id, slug):
    product = Product.objects.get(id=id, slug=slug)
    if request.method == "POST":
        product.delete()
        return redirect('my_products')
    context = {"product": product}
    return render(request, 'registration/CRUD/delete_product.html', context)


@login_required
@entrepreneur_only
def myProducts(request):
    shop = Shop.objects.get(owner=request.user)
    products = Product.objects.filter(shop=shop)
    paginator = Paginator(products, 8)
    page = request.GET.get('page')
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)
    context = {"products": objects}
    return render(request, 'registration/CRUD/my_products.html', context)


@login_required
@entrepreneur_only
def addCategory(request):
    form = CreateCategoryForm()
    if request.method == "POST":
        form = CreateCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('my_products')
    context = {'form': form}
    return render(request, 'registration/CRUD/add_category.html', context)


@login_required
def ordersHistory(request):
    orderhistory = Order.objects.filter(username=request.user).order_by('id')
    orderitem = OrderItem.objects.filter(order__in=orderhistory)
    return render(request, 'registration/order_history.html', {"orderhistory": orderhistory, "orderitem": orderitem})


@login_required
def orderHistory_detail(request, id):
    order = Order.objects.get(id=id)
    orderitem = OrderItem.objects.filter(order=order)
    if request.method == "POST":
        form = CouriersReviewForm(request.POST)
        if form.is_valid():
            new_review = form.save(commit=False)
            new_review.order = order.id
            new_review.courier = order.courier
            new_review.author = request.user
            new_review.save()
            form = CouriersReviewForm()
            messages.success(request, 'Thanks you for you review')
            return HttpResponseRedirect(request.path)
    else:
        form = CouriersReviewForm()
    return render(request, 'registration/order_history_detail.html', {"order": order, "orderitem": orderitem,
                                                                      "form": form})
