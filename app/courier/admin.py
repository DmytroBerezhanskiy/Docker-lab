from django.contrib import admin
from courier.models import Courier, CouriersReview


class CouriersReviewInline(admin.TabularInline):
    model = CouriersReview
    ordering = ('-created',)


@admin.register(Courier)
class CourierAdminModel(admin.ModelAdmin):
    list_display = ('surname', 'name', 'telephone')
    inlines = [CouriersReviewInline]
