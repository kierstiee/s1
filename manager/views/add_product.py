from django.conf import settings
from datetime import datetime, timezone
from catalog import models as cmod
from django.http import HttpResponseRedirect
from django_mako_plus import view_function, jscontext
from formlib import Formless
from django import forms


@view_function
def process_request(request):
    form = ProductForm(request)
    if form.is_valid():
        form.commit()
        return HttpResponseRedirect('/manager/list_products/')

    context = {
        'myform':form,
    }
    return request.dmp_render('add_product.html', context)


class ProductForm(Formless):

    def init(self):
        self.fields['type'] = forms.ChoiceField(label='Type', choices = cmod.Product.TYPE_CHOICES)
        self.fields['name'] = forms.CharField(label='Name')
        self.fields['description'] = forms.CharField(label='Describe the product')
        self.fields['price'] = forms.CharField(label='Price')
        self.fields['category'] = forms.ModelChoiceField(label='Category',queryset=cmod.Category.objects.all())
        self.fields['status'] = forms.ChoiceField(label='Status', choices=cmod.Product.STATUS_CHOICES)
        self.fields['quantity'] = forms.CharField(label='Quantity')
        self.fields['type'] = forms.ChoiceField(label='Type', choices = cmod.Product.TYPE_CHOICES)

        self.fields['reorder_trigger'] = forms.CharField(required=False, label='Reorder Trigger')
        self.fields['reorder_quantity'] = forms.CharField(required=False, label='Reorder Quantity')

        self.fields['itemID'] = forms.CharField(required=False, label='Item ID')

        self.fields['retire_date'] = forms.CharField(required=False, label='Retire Date')
        self.fields['max_rental_days'] = forms.CharField(required=False, label='Maximum Rental Days')

    def clean(self):
        n1 = self.cleaned_data.get('name')
        d1 = self.cleaned_data.get('description')
        p1 = self.cleaned_data.get('price')
        q1 = self.cleaned_data.get('quantity')

        if n1:
            if d1:
                if p1:
                    if q1:
                        if type == 'BulkProduct':
                            rt = self.cleaned_data.get('reorder_trigger')
                            rq = self.cleaned_data.get('reorder_quantity')
                            if rt:
                                if rq:
                                    return self.cleaned_data
                                else: raise forms.ValidationError('Please enter a reorder quantity')
                            else: raise forms.ValidationError('Please enter a reorder trigger amount')
                        elif type == 'RentalProduct':
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
                        elif type=='IndividualProduct':
                            iid = self.cleaned_data.get('itemID')
                            if not iid:
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

    def commit(self):
        p1 = self.cleaned_data.get('type')
        if p1 == 'BulkProduct':
            p2 = cmod.BulkProduct.objects.create(name=self.cleaned_data.get('name'),
                                                 description=self.cleaned_data.get('description'),
                                                 category=self.cleaned_data.get('category'),
                                                 price=self.cleaned_data.get('price'),
                                                 quantity=self.cleaned_data.get('quantity'),
                                                 status=self.cleaned_data.get('status'),
                                                 reorder_trigger=self.cleaned_data.get('reorder_trigger'),
                                                 reorder_quantity=self.cleaned_data.get('reorder_quantity'))
            p2.save()
        elif p1 == 'IndividualProduct':
            p2 = cmod.IndividualProduct.objects.create(name=self.cleaned_data.get('name'),
                                                       description=self.cleaned_data.get('description'),
                                                       category=self.cleaned_data.get('category'),
                                                       price=self.cleaned_data.get('price'),
                                                       quantity=self.cleaned_data.get('quantity'),
                                                       status=self.cleaned_data.get('status'),
                                                       itemID=self.cleaned_data.get('itemID'))
            p2.save()
        elif p1 == 'RentalProduct':
            p2 = cmod.RentalProduct.objects.create(name=self.cleaned_data.get('name'),
                                                   description=self.cleaned_data.get('description'),
                                                   category=self.cleaned_data.get('category'),
                                                   price=self.cleaned_data.get('price'),
                                                   quantity=self.cleaned_data.get('quantity'),
                                                   status=self.cleaned_data.get('status'),
                                                   itemID=self.cleaned_data.get('itemID'),
                                                   retire_date=self.cleaned_data.get('retire_date'),
                                                   max_rental_days=self.cleaned_data.get('max_rental_days'))
            p2.RentalForm.save()
        else:
            raise forms.ValidationError('Form is incorrect')
