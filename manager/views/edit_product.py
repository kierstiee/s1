from django.conf import settings
from datetime import datetime, timezone
from catalog import models as cmod
from django.http import HttpResponseRedirect
from django_mako_plus import view_function
from formlib import Formless
from django import forms


@view_function
def process_request(request, real_product:cmod.Product):
    form = Individual(real_product)
    if request.method == 'POST':
        form = Individual(request.POST, real_product)
        if form.is_valid():
            form.commit()
            return HttpResponseRedirect('/manager/list_products/')
    context = {
        'myform':form,
    }
    return request.dmp_render('edit_product.html', context)


class ProductForm(forms.ModelForm):

    class Meta:
        model = cmod.Product
        exclude = ['type']

    name = forms.CharField(initial=real_product.name)
    description = forms.CharField(initial=product.description)
    price = forms.CharField(initial=product.price)
    quantity = forms.CharField(initial=product.quantity)
    category = forms.ModelChoiceField(queryset=cmod.Category.objects.all(), empty_label='Please select one', initial=product.category)


class Individual(ProductForm):
    itemID = forms.CharField(required=False, initial=product.IndividualProduct.itemID)
    class Meta:
        model = cmod.IndividualProduct
        fields = '__all__'

    def clean(self):
        iid = self.cleaned_data.get('itemID')
        if not iid:
            raise forms.ValidationError('Please enter an item ID')
        else:
            return self.cleaned_data


class Rental(ProductForm):
    itemID = forms.CharField(required=False, initial=product.RentalProduct.itemID)
    retire_date = forms.CharField(required=False, initial=product.RentalProduct.retire_date)
    max_rental_days = forms.CharField(required=False, initial=product.RentalProduct.max_rental_days)

    class Meta:
        model = cmod.RentalProduct
        fields = '__all__'

    def clean(self):
        iid = self.cleaned_data.get('itemID')
        rd = self.cleaned_data.get('retire_date')
        mrd = self.cleaned_data.get('max_rental_days')
        if rd:
            if mrd:
                if iid:
                    return self.cleaned_data
                else:
                    raise forms.ValidationError('Please enter an item ID')
            else:
                raise forms.ValidationError('Please enter the maximum number of rental days')
        else: raise forms.ValidationError('Please enter the retire date')


class Bulk(ProductForm):
    reorder_trigger = forms.CharField(required=False, initial=product.BulkProduct.reorder_trigger)
    reorder_quantity = forms.CharField(required=False, initial=product.BulkProduct.reorder_quantity)

    class Meta:
        model = cmod.BulkProduct
        fields = '__all__'

    def clean(self):
        rt = self.cleaned_data.get('reorder_trigger')
        rq = self.cleaned_data.get('reorder_quantity')
        if rt:
            if rq:
                return self.cleaned_data
            else: raise forms.ValidationError('Please enter a reorder quantity')
        else: raise forms.ValidationError('Please enter a reorder trigger amount')
