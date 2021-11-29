from django.urls import path, include
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .decorators import unauthenticated_user

urlpatterns = [
    # path('login/', auth_views.LoginView.as_view(), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    #
    # path('password_change', auth_views.PasswordChangeView.as_view(), name='password_change'),
    # path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    #
    # path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    # path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('login/', unauthenticated_user(auth_views.LoginView.as_view()), name='login'),
    path('', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),

    path('create_product/', views.createProduct, name='create_product'),
    path('update_product/<int:id>/<slug:slug>/', views.updateProduct, name='update_product'),
    path('delete_product/<int:id>/<slug:slug>/', views.deleteProduct, name='delete_product'),

    path('my_products/', views.myProducts, name='my_products'),
    path('create_category/', views.addCategory, name='create_category'),

    path('orders_history/', views.ordersHistory, name='orders_history'),
    path('orders_history/<int:id>/', views.orderHistory_detail, name='order_detail')
]
