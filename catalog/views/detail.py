from django.conf import settings
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone
from catalog import models as cmod


@view_function
def process_request(request, id):
    product = cmod.Product.objects.get(id=id)
    c_list = cmod.Category.objects.all()
    urls = cmod.Product.image_urls(id)
    url = cmod.Product.image_url(id)
    products = request.last_five
    if product in products:
        products.remove(product)
    request.last_five = [product] + request.last_five

    context = {
        'product': product,
        'list': c_list,
        'urls': urls,
        jscontext('url'): url,
    }
    return request.dmp.render('detail.html', context)
