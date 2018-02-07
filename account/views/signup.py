from django import forms
from django.http import HttpResponseRedirect
from django.conf import settings
from django_mako_plus import view_function
from account import models as amod


@view_function
def process_request(request):
    # process form
    if request.method == 'POST':
        form = SignupForms(request.POST)
        if form.is_valid():
            # once we're here, everything is clean. No more data changes
            # do work of form (e.g., make payment, create user)
            newUser = CommitUser(form)
            return HttpResponseRedirect('/account/index/')
    else:
        form = SignupForms()
    context = {
        'form':form,
    }
    return request.dmp_render('signup.html', context)


class SignupForms(forms.Form):
    u1 = amod.User()
    u1.first_name = forms.CharField(label='First Name')
    u1.last_name = forms.CharField(label='Last Name')
    u1.email = forms.EmailField(label='Email')
    u1.password = forms.CharField(widget=forms.PasswordInput(), label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput(), label='Repeat password')

    def clean_password(self):
        password = self.cleaned_data.get('Password')
        has_digit = any([c.isdigit() for c in password])
        if len(password) < 8:
            raise forms.ValidationError('Password must have at least 8 characters. Please try again.')
        elif not has_digit:
            raise forms.ValidationError('Password must have a number. Please try again.')
        return self.cleaned_data

    def clean(self):
        # double password
        password = self.cleaned_data.get('Password')
        password2 = self.cleaned_data.get('Repeat Password')
        email = self.cleaned_data.get('Email')
        first = self.cleaned_data.get('First Name')
        last = self.cleaned_data.get('Last Name')

        if not first:
            raise forms.ValidationError('Please fill all fields')
        elif not last:
            raise forms.ValidationError('Please fill all fields')
        elif password != password2:
            raise forms.ValidationError('Passwords do not match. Please try again.')
        return self.cleaned_data

    def clean_email(self):
        email = self.cleaned_data.get('Email')
        if amod.User.objects.filter(email).exists():
            raise forms.ValidationError('This email is already registered. Do you have an account already?')
        return self.cleaned_data

class CommitUser(forms.Form):
    def commit(self):
        self.u1.save()

