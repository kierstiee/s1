from django.conf import settings
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone
from catalog import models as cmod
from account import models as amod
from decimal import Decimal
from rest_framework import serializers
from django.http import JsonResponse


@view_function
def process_request(request):
    if request.method == 'GET':
        products = cmod.Product.objects.all()
        cat = request.GET.get('category')
        name = request.GET.get('name')
        max_price = request.GET.get('price')
        if cat != '':
            cat = cmod.Category.objects.get(name__icontains=cat)
            products = products.filter(category=cat)

        if name is not None:
            products = products.filter(name__icontains=name)

        if max_price != '':
            max_price = Decimal(max_price)
            products = products.filter(price__lte=max_price)

        products = products.order_by('category','name')

        page_num = request.GET.get('page')
        max_page = int(page_num) * 6
        min_page = max_page - 6

        # products = products[max_page-5, max_page]

        products = ProductSerialize(products,many=True)
        returned = products.data[min_page: max_page]
        return JsonResponse(returned, safe=False)
    context = {
    }
    return request.dmp.render('index.html', context)


class ProductSerialize(serializers.Serializer):
    category = serializers.CharField()
    name = serializers.CharField()
    price = serializers.DecimalField(decimal_places=2, max_digits=8)

    def update(self, instance, validated_data):
        instance.category = validated_data.get('category_name', instance.category)
        instance.name = validated_data.get('name', instance.name)
        instance.price = validated_data.get('price', instance.price)
        instance.save()
        return instance
