from django import forms
from django.http import HttpResponseRedirect
from django.conf import settings
from django_mako_plus import view_function
from django.contrib.auth import authenticate, login
from account import models as amod


@view_function
def process_request(request):
    # process form
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            form.commit(request)
            return HttpResponseRedirect('/account/index/') # once we're here, everything is clean. No more data changes
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
        user = authenticate(email=self.cleaned_data.get('email'), password = self.cleaned_data.get('password'))
        # if user is None:
        #     raise forms.ValidationError('Invalid email or password')
        # else:
        return self.cleaned_data

    def commit(self, request):
        """Process the form action"""
        e1 = self.cleaned_data.get('email')
        p1 = self.cleaned_data.get('password')

        user = authenticate(email=e1, password = p1)
        if user is not None:
            login(request, user)
