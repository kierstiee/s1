from django import forms
from django.http import HttpResponseRedirect
from django.conf import settings
from django_mako_plus import view_function
from catalog import models as cmod


@view_function
def process_request(request, product:cmod.OrderItem):
    product.status='deleted'
    product.save()

    return HttpResponseRedirect('/catalog/cart/')
