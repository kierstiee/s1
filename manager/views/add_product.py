from django import forms
from django.conf import settings
from django.http import HttpResponseRedirect
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone
from catalog import models as cmod
from formlib import Formless


@view_function
def process_request(request):
    form = ProductForm(request)
    if form.is_valid():
        form.commit
        return HttpResponseRedirect('/manager/list_products/')
    context = {
        'myform':form,
    }
    return request.dmp_render('add_product.html', context)

class ProductForm(Formless):
    """Individual product"""
    class Meta:
        model = cmod.Product
