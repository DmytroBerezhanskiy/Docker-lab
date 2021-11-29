from decimal import Decimal

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from courier.models import Courier
from promocode.models import Promocode
from shop.models import Product, Shop

STATUS_CHOICES = [
    ('received', 'Received'),
    ('order collection', 'Order collection'),
    ('delivery', 'Delivery'),
    ('delivered', 'Delivered'),
    ('canceled', 'Canceled')
]


class Order(models.Model):
    username = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=50)
    address = models.CharField(max_length=100)
    telephone = models.CharField(max_length=12)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    note = models.CharField(max_length=150, null=True, blank=True)

    courier = models.ForeignKey(Courier, on_delete=models.CASCADE, null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='received')

    promocode = models.ForeignKey(Promocode, related_name="orders", null=True, blank=True, on_delete=models.SET_NULL)
    discount = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])

    class Meta:
        ordering = ('-created',)
        default_related_name = "orders"

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_price_without_discount(self):
        total_price = sum(item.get_cost() for item in self.items.all())
        return total_price

    def get_total_price(self):
        total_price = sum(item.get_cost() for item in self.items.all())
        return total_price - total_price * (self.discount / Decimal("100"))


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_item', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity

    def get_shop(self):
        shop = Product.objects.get(name=self.product).shop
        shop = Shop.objects.get(name=shop)
        return shop
