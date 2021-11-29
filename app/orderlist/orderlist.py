from django.conf import settings
from decimal import Decimal

from promocode.models import Promocode
from shop.models import Product


class OrderList(object):
    def __init__(self, request):
        self.session = request.session
        orderlist = self.session.get(settings.ORDERLIST_SESSION_ID)
        if not orderlist:
            orderlist = self.session[settings.ORDERLIST_SESSION_ID] = {}
        self.orderlist = orderlist
        self.promocode_id = self.session.get('promocode_id')

    def add(self, product, count=1, update_count=False):
        product_id = str(product.id)
        if product_id not in self.orderlist:
            self.orderlist[product_id] = {'count': 0,
                                          'price': str(product.price)}
        if update_count:
            self.orderlist[product_id]['count'] = count
        else:
            self.orderlist[product_id]['count'] += count
        self.save()

    def save(self):
        self.session[settings.ORDERLIST_SESSION_ID] = self.orderlist
        self.session.modified = True

    def delete(self, product):
        product_id = str(product.id)
        if product_id in self.orderlist:
            del self.orderlist[product_id]
            self.save()

    def __iter__(self):
        product_ids = self.orderlist.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.orderlist[str(product.id)]['product'] = product
        for item in self.orderlist.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['count']
            yield item

    def __len__(self):
        return sum(item['count'] for item in self.orderlist.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['count'] for item in self.orderlist.values())

    def clear(self):
        del self.session[settings.ORDERLIST_SESSION_ID]
        self.session.modified = True

    @property
    def promocode(self):
        if self.promocode_id:
            return Promocode.objects.get(id=self.promocode_id)
        return None

    def get_discount(self):
        if self.promocode:
            return self.promocode.discount / Decimal("100") * self.get_total_price()
        return Decimal("0")

    def get_total_price_discount(self):
        return self.get_total_price() - self.get_discount()
