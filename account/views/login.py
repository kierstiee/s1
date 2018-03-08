from django import forms
from django.http import HttpResponseRedirect
from django.conf import settings
from django_mako_plus import view_function
from account import models as amod
from django.contrib.auth import login, authenticate
from formlib import Formless
import re


@view_function
def process_request(request):
    # process form
    form = LoginForm(request)
    if form.is_valid():
        form.commit()
        return HttpResponseRedirect('/account/index/') # once we're here, everything is clean. No more data changes
    context = {
        'myform': form,
    }
    return request.dmp.render('login.html', context)


class LoginForm(Formless): # extending formlib.Form, not Django's forms.Form
    '''An example form'''
    def init(self):
        """Adds the fields for this form (called at end of __init__)"""
        self.fields['email'] = forms.EmailField(label='Email')
        self.fields['password'] = forms.CharField(widget=forms.PasswordInput, label='Password')
        self.user = None

    def clean(self):
        self.user = authenticate(email=self.cleaned_data.get('email'),password=self.cleaned_data.get('password'))
        if self.user is None:
            raise forms.ValidationError('Invalid email or password')
        return self.cleaned_data

    def commit(self):
        """Process the form action"""
        login(self.request, self.user)
