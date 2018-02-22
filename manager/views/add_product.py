from django.conf import settings
from datetime import datetime, timezone
from catalog import models as cmod
from django.http import HttpResponseRedirect
from django_mako_plus import view_function, jscontext
from formlib import Formless
from django import forms


@view_function
def process_request(request):

    if request.method == 'POST':
        form = BulkForm(request.POST)
        if form.is_valid():
            if form.type == 'BulkProduct':
                form.Bulk.commit()
            elif form.type == 'RentalProduct':
                form.Rental.commit()
            elif form.type == 'IndividualProduct':
                form.Individual.commit()
            return HttpResponseRedirect('/manager/list_products/')
    else:
        form = BulkForm()
    context = {
        'myform':form,
    }
    return request.dmp_render('add_product.html', context)


class ProductForm(forms.ModelForm):

    class Meta:
        model = cmod.Product
        fields = "__all__"

    name = forms.CharField(label='Name')
    description = forms.CharField(label='Description')
    type = forms.ChoiceField(label='Choose which type', widget=forms.Select(), choices=cmod.Product.TYPE_CHOICES)
    category = forms.ModelChoiceField(queryset=cmod.Category.objects.all(), empty_label='Please select one')


class IndividualForm(ProductForm):
    itemID = forms.CharField(required=False)

    class Meta:
        model = cmod.IndividualProduct
        fields = '__all__'

    def clean(self):
        iid = self.cleaned_data.get('itemID')
        if not iid:
            raise forms.ValidationError('Please enter an item ID')
        else:
            return self.cleaned_data


class RentalForm(ProductForm):
    itemID = forms.CharField(required=False)
    retire_date = forms.CharField(required=False)
    max_rental_days = forms.CharField(required=False)

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


class BulkForm(ProductForm):
    reorder_trigger = forms.CharField(required=False)
    reorder_quantity = forms.CharField(required=False)

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
