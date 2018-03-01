from django.conf import settings
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone
from catalog import models as cmod


@view_function
def process_request(request):
    c_list = cmod.Category.objects.all()
    context = {
        # sent to index.html:
        'list': c_list,
    }
    return request.dmp.render('index.html', context)
