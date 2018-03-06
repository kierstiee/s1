from django.conf import settings
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone


@view_function
def process_request(request):
    utc_time = datetime.utcnow()
    quote = 'Lorem ipsum dolor sit amet, consectetaur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua'
    context = {
        # sent to index.html:
        'welcome': 'Welcome to FOMO!',
        'welcome2': 'Our family-run business is dedicated to providing you with the best musical experience in Utah Valley!',
        'text': quote,
    }
    return request.dmp.render('index.html', context)

