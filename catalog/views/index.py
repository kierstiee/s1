from django.conf import settings
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone
from catalog import models as cmod
import math


@view_function
def process_request(request, id=0):
    c_list = cmod.Category.objects.all()
    if int(id) > 0:
        catalog = cmod.Category.objects.get(id=id)
        name = catalog.name
        category=catalog
        p_list = cmod.Product.objects.filter(category=category)
    else:
        name = 'Products'
        catalog = cmod.Category.objects.all()
        category=None
        p_list = cmod.Product.objects.all()

    num_pages = p_list.count()/6
    num_pages = math.ceil(num_pages)

    context = {
        # sent to index.html:
        'list': c_list,
        'catalog': catalog,
        'name': name,
        'category': category,
        'p_list': p_list,
        'num_pages': num_pages,
        jscontext('num_pages'): num_pages,
        jscontext('cid'): id,
    }
    return request.dmp.render('index.html', context)


@view_function
def products(request, cat:cmod.Category=None, pnum:int=0):
    qry = cmod.Product.objects.all()
    p_list = cmod.Product.objects.all()
    if cat is not None:
        qry = qry.filter(category=cat)
        p_list = p_list.filter(category=cat)
    num_pages = math.ceil(p_list.count()/6)
    qry = qry[pnum*6:(pnum+1)*6]
    context = {
        'qry': qry,
        'pnum': pnum+1,
        'num_pages': num_pages,
    }
    return request.dmp.render('index.products.html',context)
