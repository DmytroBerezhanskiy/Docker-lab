from django import template
from shop.models import Shop

register = template.Library()


@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()


@register.filter(name='has_shop')
def has_shop(user, shop_name):
    if Shop.objects.filter(owner=user):
        if Shop.objects.get(owner=user).name == shop_name.name:
            return shop_name.name
    else:
        return None
