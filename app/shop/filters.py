import django_filters
from django_filters import NumberFilter, RangeFilter, CharFilter, OrderingFilter
from .models import Product


class ProductFilter(django_filters.FilterSet):
    price_start = NumberFilter(field_name='price', lookup_expr='gte')
    price_end = NumberFilter(field_name='price', lookup_expr='lte')
    name = CharFilter(field_name='name', lookup_expr='icontains')
    # price = RangeFilter(field_name='price')
    ordering = OrderingFilter(
        fields=(
            ('price', 'by price'),
            ('name', 'by name'),
            ('created', 'by created'),
        )
    )

    class Meta:
        model = Product
        fields = ('category', 'name')
        exclude = ['price', 'name']
