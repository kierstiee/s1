from django.conf import settings
from datetime import datetime, timezone
from catalog import models as cmod
from django.http import HttpResponseRedirect
from django_mako_plus import view_function, jscontext
from formlib import Formless
from django import forms


@view_function
def process_request(request, real_product:cmod.Product):
    start = forms.model_to_dict(real_product)
    form = ProductForm(request, initial=start)
    if form.is_valid():
        form.commit(real_product)
        return HttpResponseRedirect('/manager/list_products/')
    title = real_product.TITLE
    context = {
        'myform': form,
        jscontext('title'): title
    }
    return request.dmp_render('edit_product.html', context)


class ProductForm(Formless):

    def init(self):

        self.fields['name'] = forms.CharField(label='Name')
        self.fields['description'] = forms.CharField(label='Describe the product')
        self.fields['price'] = forms.CharField(label='Price')
        self.fields['category'] = forms.ModelChoiceField(label='Category',queryset=cmod.Category.objects.all())
        self.fields['status'] = forms.ChoiceField(label='Status', choices=cmod.Product.STATUS_CHOICES)
        self.fields['quantity'] = forms.CharField(label='Quantity')

        self.fields['reorder_trigger'] = forms.CharField(required=False, label='Reorder Trigger')
        self.fields['reorder_quantity'] = forms.CharField(required=False, label='Reorder Quantity')

        self.fields['itemID'] = forms.CharField(required=False, label='Item ID')

        self.fields['retire_date'] = forms.DateField(required=False, label='Retire Date')
        self.fields['max_rental_days'] = forms.CharField(required=False, label='Maximum Rental Days')

    def clean(self):
        n1 = self.cleaned_data.get('name')
        d1 = self.cleaned_data.get('description')
        p1 = self.cleaned_data.get('price')
        q1 = self.cleaned_data.get('quantity')
        queryset = cmod.Product.objects.filter(name=self.cleaned_data.get('name'))
        checktype = queryset.reverse()[0]
        t1 = checktype.TITLE
        rt = self.cleaned_data.get('reorder_trigger')
        rq = self.cleaned_data.get('reorder_quantity')
        iid = self.cleaned_data.get('itemID')
        rd = self.cleaned_data.get('retire_date')
        mrd = self.cleaned_data.get('max_rental_days')
        if n1:
            if d1:
                if p1:
                    if q1:
                        if t1 == 'BulkProduct':
                            if rt != '':
                                if rq != '':
                                    return self.cleaned_data
                                else: raise forms.ValidationError('Please enter a reorder quantity')
                            else: raise forms.ValidationError('Please enter a reorder trigger amount')
                        elif t1 == 'RentalProduct':
                            if rd != None:
                                if mrd != '':
                                    if iid != '':
                                        return self.cleaned_data
                                    else: raise forms.ValidationError('Please enter an item ID')
                                else: raise forms.ValidationError('Please enter the maximum number of rental days')
                            else: raise forms.ValidationError('Please enter the retire date')
                        elif t1 == 'IndividualProduct':
                            if iid == '':
                                raise forms.ValidationError('Please enter an item ID')
                            else:
                                return self.cleaned_data
                    else:
                        raise forms.ValidationError('Please enter the quantity')
                else:
                    raise forms.ValidationError('Please enter the price')
            else:
                raise forms.ValidationError('Please enter the description')
        else:
            raise forms.ValidationError('Please enter the name')

    def commit(self,product):
        p1 = product.TITLE
        product.name=self.cleaned_data.get('name')
        product.description=self.cleaned_data.get('description')
        product.category=self.cleaned_data.get('category')
        product.price=self.cleaned_data.get('price')
        product.quantity=self.cleaned_data.get('quantity')
        product.status=self.cleaned_data.get('status')
        if p1 == 'BulkProduct':
            product.reorder_trigger=self.cleaned_data.get('reorder_trigger')
            product.reorder_quantity=self.cleaned_data.get('reorder_quantity')
            product.save()
        elif p1 == 'IndividualProduct':
            product.itemID=self.cleaned_data.get('itemID')
            product.save()
        elif p1 == 'RentalProduct':
            product.itemID=self.cleaned_data.get('itemID')
            product.retire_date=self.cleaned_data.get('retire_date')
            product.max_rental_days=self.cleaned_data.get('max_rental_days')
            product.save()
        else:
            raise forms.ValidationError('Form is incorrect')
