from django.conf import settings
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone
from catalog import models as cmod
from account import models as amod
import traceback
from formlib import Formless
from django import forms
from django.http import HttpResponseRedirect


@view_function
def process_request(request):
    c_list = cmod.Category.objects.all()
    user = request.user
    order = amod.User.get_shopping_cart(user)
    order.recalculate()
    order.save()
    total = round(order.total_price, 2)
    form = ShippingClass(request,order=order)
    if form.is_valid():
        form.commit()
        return HttpResponseRedirect('/catalog/thanks/')

    context = {
        'c_list': c_list,
        'order': order,
        'total': total,
        'form': form
    }
    return request.dmp.render('checkout.html', context)


class ShippingClass(Formless):
    def __init__(self, *args, **kwargs):
        self.order = kwargs.pop('order')
        super(ShippingClass, self).__init__(*args, **kwargs)

    def init(self):
        self.fields['address'] = forms.CharField(label="Address")
        self.fields['city'] = forms.CharField(label="City")
        self.fields['state'] = forms.CharField(label="State")
        self.fields['zip'] = forms.IntegerField(label="Zip", max_value=99999, min_value=10000)
        self.fields['stripeToken'] = forms.CharField(widget=forms.HiddenInput)

    def clean(self):
        a1 = self.cleaned_data.get('address')
        c1 = self.cleaned_data.get('city')
        s1 = self.cleaned_data.get('state')
        z1 = self.cleaned_data.get('zip')
        sT = self.cleaned_data.get('stripeToken')
        if a1:
            if c1:
                if s1:
                    if z1:
                        if sT:
                            return self.cleaned_data
                        else:
                            raise forms.ValidationError("Missing the token")
                            traceback.print_exc()
                    else: raise forms.ValidationError("Please enter a zip code")
                else: raise forms.ValidationError("Please enter a state")
            else: raise forms.ValidationError("Please enter a city")
        else: raise forms.ValidationError("Please enter an address")

    def commit(self):
        order = self.order
        order.ship_address = self.cleaned_data.get('address')
        order.ship_city = self.cleaned_data.get('city')
        order.ship_state = self.cleaned_data.get('state')
        order.ship_zip_code = self.cleaned_data.get('zip')
        try:
            order.finalize(self.cleaned_data.get('stripeToken'))
        except:
            raise forms.ValidationError("Didn't work")
            traceback.print_exc()
        order.save()
