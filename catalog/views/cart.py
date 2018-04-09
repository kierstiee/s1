from django.conf import settings
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone
from account import models as amod
from catalog import models as cmod
from decimal import Decimal
from formlib import Formless
import math


@view_function
def process_request(request):
    c_list = cmod.Category.objects.all()
    order = amod.User.get_shopping_cart(request.user)
    active_list = cmod.Order.active_items(order, include_tax_item=True)
    # tax = cmod.Product.object.get(name='Tax Item')
    for item in active_list:
        item.recalculate()
        item.save()
    order.recalculate()
    order.save()
    order_total = round(order.total_price,2)
    tax = order_total - round(order_total / Decimal(1.07), 2)

    context = {
        # sent to index.html:
        'c_list': c_list,
        'active': active_list,
        'tax': tax,
        'total': order_total,
        'order': order,
    }
    return request.dmp.render('cart.html', context)
