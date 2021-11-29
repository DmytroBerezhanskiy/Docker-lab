from django import forms
from django.contrib.auth.models import User
from .models import UserProfile
from shop.models import Product, Shop, Category

TYPE_REGISTER = [
    ('customer', 'Customer'),
    ('entrepreneur', 'Entrepreneur'),
]


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class ShopRegistrationForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ['name']
        labels = {
            "name": "Restaurant name"
        }

    def __init__(self, *args, **kwargs):
        super(ShopRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['name'].required = False


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password_repeat = forms.CharField(label='Repeat password', widget=forms.PasswordInput)
    register_like = forms.CharField(label='Register as:', required=True,
                                    widget=forms.RadioSelect(choices=TYPE_REGISTER))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def clean_password_repeat(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password_repeat']:
            raise forms.ValidationError('Passwords don\'t match')
        return cd['password_repeat']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('telephone', 'address', 'birthday')


class CreateProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['shop', 'category', 'name', 'price', 'image', 'description', 'available']


class CreateCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
