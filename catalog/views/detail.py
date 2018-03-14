from django.conf import settings
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone
from catalog import models as cmod


@view_function
def process_request(request, id):
    product = cmod.Product.objects.get(id=id)
    context = {
        'product': product
    }
    return request.dmp.render('detail.html', context)
