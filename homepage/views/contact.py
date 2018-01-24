from django.conf import settings
from django_mako_plus import view_function, jscontext

@view_function
def process_request(request):

    if request.method == 'POST':
        print(request.POST['firstname'], request.POST['lastname'] , request.POST['email'], request.POST['comment'])

    context = {
    }
    return request.dmp_render('contact.html', context)
