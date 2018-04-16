from django.conf import settings
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone
from catalog import models as cmod
from account import models as amod
from rest_framework import generics
from rest_framework.response import Response


class ProductSearch(generics.ListAPIView):
    def get_queryset(self):
        """This view returns a list of all the products the user is searching for"""
        products = cmod.Product.objects.all()

        category = self.request.query_params.get('category', None)
        if category is not None:
            products = products.filter(category__icontains=category)

        name = self.request.query_params.get('name', None)
        if name is not None:
            products = products.filter(name__icontains=name)

        max_price = self.request.query_params.get('price',None)
        if max_price is not None:
            products = products.filter(price__lte=max_price)

        products.order_by('category','name')

        page_no = self.request.query_params.get('page', 1)

        return Response(products)
