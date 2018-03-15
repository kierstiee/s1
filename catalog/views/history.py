from django.conf import settings
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone
from catalog import models as cmod

class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        # before the request:
        # requestion.session -> DIctionary
        # product_ids = session.get ids from the session
        # products = [convert list of ids to actual objects]
        # request.last_five = [product objects]

        # in catalog/templates/app_base.htm:

        # do for-loop through the last five, print out images

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
