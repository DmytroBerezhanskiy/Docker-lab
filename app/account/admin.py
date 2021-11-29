from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdminModel(admin.ModelAdmin):
    list_display = ('user', 'telephone', 'address', 'birthday')
