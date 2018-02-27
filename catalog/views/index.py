from django.conf import settings
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone
from catalog import models as cmod


@view_function
def process_request(request):
    utc_time = datetime.utcnow()
    context = {
        # sent to index.html:
        'utc_time': utc_time,
    }
    return request.dmp.render('index.html', context)
