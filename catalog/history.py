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

        # request.session -> DIctionary
        products = []
        # product_ids = request.session.get(id,'326')
        #
        # products.append(cmod.Product.objects.get(id=product_ids[id])
        products.reverse()
        request.last_five = islice(products, 6)

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
