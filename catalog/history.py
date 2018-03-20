from django.conf import settings
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone
from catalog import models as cmod
from itertools import islice


class LastFiveMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        product_ids = request.session.get('last_5',['326','327','328','329','330','331','332'])
        products = []
        for ids in product_ids:
            ids = int(ids)
            products.append(cmod.Product.objects.get(id=ids))
        request.last_five = products[:6]

        response = self.get_response(request) # what calls the view

        pids = []
        for product in request.last_five:
            pids.append(product.id)
        new_pids = pids[:6]
        request.session['last_5'] = new_pids

        return response
