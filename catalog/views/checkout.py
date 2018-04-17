from django.conf import settings
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone
from catalog import models as cmod
from account import models as amod
import math


@view_function
def process_request(request):
    c_list = cmod.Category.objects.all()
    order = amod.User.get_shopping_cart(request.user)
    order.recalculate()
    order.save()
    total = round(order.total_price, 2)
    context = {
        'c_list': c_list,
        'order': order,
        'total': total,
    }
    return request.dmp.render('checkout.html', context)
