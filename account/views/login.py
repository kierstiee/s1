from django import forms
from django.http import HttpResponseRedirect
from django.conf import settings
from django_mako_plus import view_function


@view_function
def process_request(request):
    # process form
    if request.method == 'POST':
        form = TestForm(request.POST)
        if form.is_valid():
            # do work of form (e.g., make payment, create user)

            return HttpResponseRedirect('/')
    else:
        form = TestForm()

        context = {
            'form':form,
        }
    return request.dmp_render('login.html', context)

class TestForm(forms.Form):
    favorite_ice_cream = forms.CharField(label = 'Favorite Ice Cream')
    renewal_date = forms.DateField(label="Renewal", help_text="Please enter a date between nnow and 4 weeks (default 3).")
