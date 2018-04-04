from django.conf import settings
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone
from account import models as amod
from catalog import models as cmod
from formlib import Formless
import math


@view_function
def process_request(request):
    c_list = cmod.Category.objects.all()
    order = amod.User.get_shopping_cart(request.user)
    active_list = cmod.Order.active_items(order, include_tax_item=True)
    context = {
        # sent to index.html:
        'c_list': c_list,
        'active': active_list,
    }
    return request.dmp.render('cart.html', context)
