from django.conf import settings
import traceback
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone
from catalog import models as cmod
from account import models as amod
from formlib import Formless
from django.forms import ValidationError


@view_function
def process_request(request):
    c_list = cmod.Category.objects.all()
    order = amod.User.get_shopping_cart(request.user)
    token = request.form['stripeToken']
    form = CartForm(request,order,token)

    context = {
        'c_list': c_list,
        'order': order,
    }
    return request.dmp.render('checkout.html', context)


class CartForm(Formless):

    def __init__(self, *args, **kwargs):
        self.order = kwargs.pop('order')
        self.token = kwargs.pop('token')
        super(CartForm, self).__init__(*args, **kwargs)


    def init(self):
        self.fields['order'] = self.order
        self.fields['token'] = self.token

    def clean(self):
        o1 = self.cleaned_data.get('order')
        t1 = self.cleaned_data.get('token')
        if t1:
            if o1:
                o1.finalize(t1)
                return self.cleaned_data
            else:
                raise ValidationError('Missing the order')
                traceback.print_exc()
        else: raise ValidationError('missing the token')
        traceback.print_exc()
