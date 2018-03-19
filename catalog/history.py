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
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        # request.session -> Dictionary
        # product_ids = session.get ids from the session
        product_ids = request.session.get('last_5',['326','326','326','326','326','326','326'])
        products = []
        # products = [ convert list of ids to actual objects ]
        for ids in product_ids:
            ids = int(ids)
            products.append(cmod.Product.objects.get(id=ids))
        products.reverse()
        # request.last_five = [ product objects ]
        request.last_five = islice(products,6)

        response = self.get_response(request) # what calls the view
        # Code to be executed for each request/response after
        # the view is called.

        # convert request last_five to list of ids
        pids = []
        for product in request.last_five:
            pids.append(product.id)
            # set the list of ids into the session
        request.session['listof5'] = pids

        return response
