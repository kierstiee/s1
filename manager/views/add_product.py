from django.conf import settings
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone
from catalog import models as cmod


@view_function
def process_request(request):

    context = {
    }
    return request.dmp_render('add_product.html', context)
