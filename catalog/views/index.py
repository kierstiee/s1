from django.conf import settings
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone
from category import models as cmod


@view_function
def process_request(request, product:cmod.Product=0):
    utc_time = datetime.utcnow()
    context = {
        # sent to index.html:
        'utc_time': utc_time,
        # sent to index.html and index.js:
        jscontext('utc_epoch'): utc_time.timestamp(),
    }
    return request.dmp.render('index.html', context)
