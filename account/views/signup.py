from django import forms
from django.http import HttpResponseRedirect
from django.conf import settings
from django_mako_plus import view_function
from account import models as amod
from django.contrib.auth import login, authenticate
import re


@view_function
def process_request(request):
    # process form

    if request.method == 'POST':
        form = SignupForms(request.POST)
        if form.is_valid():
            # once we're here, everything is clean. No more data changes
            # do work of form (e.g., make payment, create user)
            form.commit(request)
            return HttpResponseRedirect('/account/index/')
    else:
        form = SignupForms()

    context = {
        'myform': form,
    }
    return request.dmp_render('signup.html', context)


class SignupForms(forms.Form):
    email = forms.EmailField(label='Email')
    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Repeat password')

    def clean_password(self):
        p1 = self.cleaned_data.get('password')
        has_digit = any([c.isdigit() for c in p1])
        if len(p1) < 8:
            raise forms.ValidationError('Password must have at least 8 characters. Please try again.')
        elif not has_digit:
            raise forms.ValidationError('Password must have a number. Please try again.')
        return self.cleaned_data

    def clean(self):
        # double password
        p1 = self.cleaned_data.get('password')
        p2 = self.cleaned_data.get('password2')
        # if str(p1) != str(p2):
        #     raise forms.ValidationError('Passwords do not match. Please try again.')
        return self.cleaned_data

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if amod.User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already registered. Do you have an account already?')
        return self.cleaned_data

    def commit(self, request):
        newuser = amod.User()
        newuser.email = self.cleaned_data.get('email')
        newuser.set_password(self.cleaned_data.get('password'))
        newuser.first_name = self.cleaned_data.get('first_name')
        newuser.last_name = self.cleaned_data.get('last_name')

        newuser.save()
        login(request, newuser)
