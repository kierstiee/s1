from django import forms
from django.http import HttpResponseRedirect
from django.conf import settings
from django_mako_plus import view_function
from django.contrib.auth import authenticate, login



@view_function
def process_request(request):
    # process form
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # once we're here, everything is clean. No more data changes
            # do work of form (e.g., make payment, create user)

            return HttpResponseRedirect('/account/index/')
    else:
        form = LoginForm()

    context = {
        'myform': form,
    }
    return request.dmp_render('login.html', context)

class LoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(widget=forms.PasswordInput(), label='Password')

    def clean(self):
        user = authenticate(email = self.email, password = self.password)
        if user is None:
            raise forms.ValidationError('This email is not registered with our website. Please go to Signup')
        else:
            return self.cleaned_data

    def commit(self):
        """Process the form action"""
        user = authenticate(email = self.email, password = self.password)
        login(self.request, user)
        # login()
