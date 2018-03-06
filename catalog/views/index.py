from django.conf import settings
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone
from catalog import models as cmod


@view_function
def process_request(request, id=0):
    c_list = cmod.Category.objects.all()
    if int(id) > 0:
        catalog = cmod.Category.objects.get(id=id)
        name = catalog.name
        category=catalog
        p_list = cmod.Product.objects.filter(category=category)
        for product in p_list:
            pic_list = cmod.ProductImage.objects.filter(product=product)
    else:
        name = 'Products'
        catalog = cmod.Category.objects.all()
        category=None
        p_list = cmod.Product.objects.all()
        for product in p_list:
            pic_list = cmod.ProductImage.objects.filter(product=product)

    context = {
        # sent to index.html:
        'list': c_list,
        'catalog': catalog,
        'name': name,
        'category': category,
        'p_list': p_list,
        'pic_list': pic_list,
    }
    return request.dmp.render('index.html', context)
