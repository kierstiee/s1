from django.conf import settings
from datetime import datetime, timezone
from catalog import models as cmod
from django.http import HttpResponseRedirect
from formlib import Formless
from django_mako_plus import view_function, jscontext
from django import forms
from account import models as amod
from django.contrib.auth.decorators import permission_required


# @permission_required(cmod.Product.objects.all())
@view_function
def process_request(request, id):
    product = cmod.Product.objects.get(id=id)
    c_list = cmod.Category.objects.all()
    urls = cmod.Product.image_urls(id)
    url = cmod.Product.image_url(id)
    products = request.last_five
    user = request.user
    if product in products:
        products.remove(product)
    request.last_five = [product] + request.last_five

    if product.TITLE == 'BulkProduct':
        form = AddBulkProduct(request, product=product, user=user)
    else:
        form = AddProduct(request, product=product, user=user)

    if form.is_valid():
        form.commit()
        return HttpResponseRedirect('/catalog/cart/')

    quan1 = 0
    order = amod.User.get_shopping_cart(request.user)
    active = cmod.Order.active_items(order, include_tax_item=False)
    for item in active:
        if item == product:
            quan1 = quan1 + item.quantity


    context = {
        'product': product,
        'c_list': c_list,
        'urls': urls,
        jscontext('url'): url,
        'form': form,
        'q1': quan1,
        'order': order,
    }
    return request.dmp.render('detail.html', context)


class AddBulkProduct(Formless):

    def __init__(self, *args, **kwargs):
        self.product = kwargs.pop('product')
        self.user = kwargs.pop('user')
        super(AddBulkProduct, self).__init__(*args, **kwargs)

    def init(self):
        self.fields['quantity']=forms.IntegerField(label="Quantity of Order")

    def clean(self):
        q1 = self.cleaned_data.get('quantity')
        order = amod.User.get_shopping_cart(self.user)
        active = cmod.Order.active_items(order, include_tax_item=False)
        q2 = 0
        for item in active:
            if self.product == item:
                q2 = q2 + item.quantity
        if q1:
            if q1 < self.product.quantity:
                return self.cleaned_data
            else: raise forms.ValidationError('There are not enough to fulfill this order. Please try again later.')
        else: raise forms.ValidationError('Please enter a quantity')

    def commit(self):
        q1 = self.cleaned_data.get('quantity')
        product = self.product
        order = amod.User.get_shopping_cart(self.user)
        active = cmod.Order.active_items(order, include_tax_item=False)
        for item in active:
            if product == item.product:
                q1 = q1 + item.quantity
        item = cmod.Order.get_item(order, self.product, create=True)
        item.quantity = q1
        item.save()


class AddProduct(Formless):

    def __init__(self, *args, **kwargs):
        self.product = kwargs.pop('product')
        self.user = kwargs.pop('user')
        super(AddProduct, self).__init__(*args, **kwargs)

    def commit(self):
        product = self.product
        user = self.user
        order = amod.User.get_shopping_cart(user)
        item = cmod.Order.get_item(order, product, create=True)
        item.quantity = 1
        item.save()
        product.status = 'I'
        product.save()
