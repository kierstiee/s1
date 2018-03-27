from django.conf import settings
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone
from catalog import models as cmod
from formlib import Formless
import math


@view_function
def process_request(request, id=0, quantity=1):
    c_list = cmod.Category.objects.all()
    product = cmod.Product.objects.get(id=id)
    item = cmod.Order.get_item(product, create=True)
    context = {
        # sent to index.html:
        'c_list': c_list,
        'item': item,
    }
    return request.dmp.render('cart.html', context)


class CartForm(Formless):

    def init(self):
        self.fields

    def clean(self):
