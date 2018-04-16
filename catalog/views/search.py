from django.conf import settings
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone
from catalog import models as cmod
from account import models as amod
from rest_framework import serializers
from rest_framework import generics
from rest_framework.response import Response
from django.http import JsonResponse


@view_function
def process_request(request):
    if request.method == 'GET':
        products = cmod.Product.objects.all()
        products = ProductSerialize(products,many=True)
        return JsonResponse(products.data, safe=False)
    context = {

    }
    return request.dmp.render('index.html', context)

class ProductSerialize(serializers.Serializer):
    category = serializers.CharField()
    name = serializers.CharField()
    price = serializers.DecimalField(decimal_places=2, max_digits=8)

    def create(self, validated_data):
        return ProductSearch()

    def update(self, instance, validated_data):
        instance.category = validated_data.get('category_name', instance.category)
        instance.name = validated_data.get('name', instance.name)
        instance.price = validated_data.get('price', instance.price)
        instance.save()
        return instance


class ProductSearch(generics.ListAPIView):
    """This view returns a list of all the products the user is searching for in JSON"""
    serializer_class = ProductSerialize

    def get_queryset(self):
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
