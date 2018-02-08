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
    form = SignupForm(request)
    if form.is_valid():
        form.commit()
        return HttpResponseRedirect('/account/index/') # once we're here, everything is clean. No more data changes
    context = {
        'myform': form,
    }
    return request.dmp_render('signup.html', context)


class SignupForm(Formless):   # extending formlib.Form, not Django's forms.Form
    '''An example form'''
    def init(self):
        """Adds the fields for this form (called at end of __init__)"""
        self.fields['email'] = forms.EmailField(label='Email')
        self.fields['first_name'] = forms.CharField(label='First Name')
        self.fields['last_name'] = forms.CharField(label='Last Name')
        self.fields['password'] = forms.CharField(widget=forms.PasswordInput, label='Password')
        self.fields['password2'] = forms.CharField(widget=forms.PasswordInput, label='Repeat password')
        self.user = None

    def clean_password(self):
        p1 = self.cleaned_data.get('password')
        has_digit = any([c.isdigit() for c in p1])
        if len(p1) < 8:
            raise forms.ValidationError('Password must have at least 8 characters. Please try again.')
        elif not has_digit:
            raise forms.ValidationError('Password must have a number. Please try again.')
        return p1

    def clean(self):
        # double password
        p1 = self.cleaned_data.get('password')
        p2 = self.cleaned_data.get('password2')
        if p1 != p2:
            raise forms.ValidationError('Passwords must match')
        return self.cleaned_data

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if amod.User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already registered. Do you have an account already?')
        return email

    def commit(self):
        u1 = amod.User.objects.create(email=self.cleaned_data.get('email'),
                                      first_name=self.cleaned_data.get('first_name'),
                                      last_name=self.cleaned_data.get('last_name'))
        u1.set_password(self.cleaned_data.get('password'))
        u1.save()
        login(self.request, u1)
