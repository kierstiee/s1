from django.conf import settings
from datetime import datetime, timezone
from catalog import models as cmod
from django.http import HttpResponseRedirect
from django_mako_plus import view_function
from formlib import Formless
from django import forms


@view_function
def process_request(request, product:cmod.Product):
    form = ProductForm(request, product)
    if form.is_valid():
        form.commit
        return HttpResponseRedirect('/manager/list_products/')
    context = {
        'myform':form,
    }
    return request.dmp_render('edit_product.html', context)


class ProductForm(Formless, product):
    """Individual product"""
    def init(self):
        self.fields['name'] = forms.CharField(label='Name', initial=product.name)
        self.fields['price'] = forms.CharField(label='Price', initial=product.price)
        self.fields['description'] = forms.CharField(label='Describe the product', initial=product.description)
        self.fields['category'] = forms.ModelChoiceField(label='Category',queryset=cmod.Category.name, initial=product.category)
        self.fields['status'] = forms.ChoiceField(label='Status', initial=product.status)
        self.fields['quantity'] = forms.CharField(label='Quantity', initial=product.quantity)
        self.fields['reorder_trigger'] = forms.CharField(label='Reorder Trigger', initial=product.BulkProduct.reorder_trigger)
        self.fields['reorder_quantity'] = forms.CharField(label='Reorder Quantity', initial=product.BulkProduct.reorder_quantity)
        self.fields['itemID'] = forms.CharField(label='Item ID', initial=product.IndividualProduct.itemID)
        self.fields['itemID'] = forms.CharField(label='Item ID', initial=product.RentalProduct.itemID)
        self.fields['retire_date'] = forms.CharField(label='Retire Date', initial=product.RentalProduct.retire_date)
        self.fields['max_rental_days'] = forms.CharField(label='Maximum Rental Days', initial=product.RentalProduct.max_rental_days)
