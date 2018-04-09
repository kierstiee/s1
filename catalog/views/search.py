from django.conf import settings
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone
from catalog import models as cmod
from account import models as amod


@view_function
def process_request(request):
    query = request.GET.get('q')
    products = cmod.Product.objects.filter(name__icontains=query)
    c_list = cmod.Category.objects.all()
    order = amod.User.get_shopping_cart(request.user)
    context = {
        'products': products,
        'c_list': c_list,
        'order': order,
    }
    return request.dmp.render('search.html', context)
