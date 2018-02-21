from django.conf import settings
from datetime import datetime, timezone
from catalog import models as cmod
from django.http import HttpResponseRedirect
from django_mako_plus import view_function
from formlib import Formless
from django import forms

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
    def init(self):
        self.fields['name'] = forms.CharField(label='Name')
        self.fields['price'] = forms.CharField(label='Price')
        self.fields['description'] = forms.CharField(label='Describe the product')
        self.fields['category'] = forms.ModelChoiceField(label='Category',queryset=cmod.Category.name)
        self.fields['status'] = forms.ChoiceField(label='Status')
        self.fields['quantity'] = forms.CharField(label='Quantity')
        self.fields['type'] = forms.ChoiceField(label='Type of product')
        self.fields['reorder_trigger'] = forms.CharField(label='Reorder Trigger')
        self.fields['reorder_quantity'] = forms.CharField(label='Reorder Quantity')
        self.fields['itemID'] = forms.CharField(label='Item ID')
        self.fields['itemID'] = forms.CharField(label='Item ID')
        self.fields['retire_date'] = forms.CharField(label='Retire Date')
        self.fields['max_rental_days'] = forms.CharField(label='Maximum Rental Days')
