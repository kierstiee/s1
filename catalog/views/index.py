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

    else:
        name = 'Products'
        catalog = cmod.Category.objects.all()
        category=None

    context = {
        # sent to index.html:
        'list': c_list,
        'catalog': catalog,
        'name': name,
        'category': category,
    }
    return request.dmp.render('index.html', context)
