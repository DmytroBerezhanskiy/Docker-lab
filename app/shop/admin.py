from django.contrib import admin
from django.contrib.admin import RelatedFieldListFilter
from django.contrib.admin.models import LogEntry
from .models import Category, Product, Shop, Reviews, ReviewsAnswer
from django.contrib.auth.models import User


class ReviewsInline(admin.TabularInline):
    model = Reviews
    ordering = ('-created',)


@admin.register(Reviews)
class ReviewsAdminModel(admin.ModelAdmin):
    list_display = ('id', 'product', 'rating', 'created', 'show')
    ordering = ('created',)


@admin.register(ReviewsAnswer)
class ReviewsAnswerAdminModel(admin.ModelAdmin):
    list_display = ('review', 'author', 'body', 'created')
    ordering = ('review',)

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(Shop)
class ShopAdminModel(admin.ModelAdmin):
    list_display = ('name', 'slug', 'owner')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)


@admin.register(Category)
class CategoryAdminModel(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)


@admin.register(Product)
class ProductAdminModel(admin.ModelAdmin):
    list_display = ('name', 'shop', 'category', 'slug', 'price', 'available', 'image', 'created', 'updated',)
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)
    list_filter = ['available', 'created', 'updated']
    list_editable = ('price', 'available', 'image',)
    inlines = [ReviewsInline]


class SuperUserFilter(admin.SimpleListFilter):
    title = 'user'
    parameter_name = 'user'

    def lookups(self, request, model_admin):
        superusers = []
        qs = User.objects.filter(is_superuser=True)
        for superuser in qs:
            superusers.append([superuser.id, superuser.username])
        return superusers

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(user__id__exact=self.value())
        else:
            return queryset


@admin.register(LogEntry)
class LogAdminModel(admin.ModelAdmin):
    list_display = ('action_time', 'user', 'content_type', 'change_message', 'is_addition', 'is_change', 'is_deletion')
    list_filter = ['action_time', SuperUserFilter, 'content_type']
    ordering = ('-action_time',)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
