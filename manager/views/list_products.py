from django.conf import settings
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone
from catalog import models as cmod


@view_function
def process_request(request):
    product_list = cmod.Product.objects.filter(status = 'A')
    context = {
        'product_list':product_list
    }
    return request.dmp.render('list_products.html', context)
