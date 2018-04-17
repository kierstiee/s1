from django.conf import settings
import traceback
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone
from catalog import models as cmod
from account import models as amod
from formlib import Formless
from django.forms import ValidationError


@view_function
def process_request(request, token):
    c_list = cmod.Category.objects.all()
    order = amod.User.get_shopping_cart(request.user)

    context = {
        'c_list': c_list,
        'order': order,
    }
    return request.dmp.render('thanks.html', context)
