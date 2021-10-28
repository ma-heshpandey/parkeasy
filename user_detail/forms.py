from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView
from django.contrib.auth import authenticate,login
from django.http import HttpResponseRedirect
from django.db import models
from django.core.exceptions import ValidationError


class UserForm(UserCreationForm):


    class Meta:
        model=User
        fields=['username','first_name','last_name','mobile_number','email','password1','password2']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder':'User Name','stye':'border-radius:4px' }),
            'first_name': forms.TextInput(attrs={'placeholder':'First Name' }),
            'last_name': forms.TextInput(attrs={'placeholder':'Last Name' }),
            'mobile_number': forms.TextInput(attrs={'placeholder':'Mobile Number' }),
            'email': forms.TextInput(attrs={'placeholder':'Email' }),
            'password1': forms.TextInput(attrs={'placeholder':'Password1' }),
            'password2': forms.TextInput(attrs={'placeholder':'Password Confirmation' }),
        }

class UserFormForAdmin(UserCreationForm):

    class Meta:
        model=User
        fields=['username','first_name','last_name','mobile_number','email','password1','password2',]

        widgets={
            'username': forms.TextInput(attrs={'placeholder': 'User Name', 'stye': 'border-radius:4px'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'mobile_number': forms.TextInput(attrs={'placeholder': 'Mobile Number'}),
            'email': forms.TextInput(attrs={'placeholder': 'Email'}),
            'password1': forms.TextInput(attrs={'placeholder': 'Password1'}),
            'password2': forms.TextInput(attrs={'placeholder': 'Password Confirmation'}),
            'admin':forms.TextInput(attrs={'type':'hidden','value':'True',}),
        }

    # def clean_email(self):
    #     # Get the field value from cleaned_data dict
    #     email = self.cleaned_data['email']
    #     # Check if the value end in @hotmail.com
    #     if User.objects.filter(email=email).exists():
    #     # Value ends in @hotmail.com, raise an error
    #         raise forms.ValidationError("Email already exit")
    #     return email

class UserSignUp(SuccessMessageMixin,CreateView):
     model = User
     form_class = UserForm
     success_url = reverse_lazy('/')
     success_message = "User created successfully"
     template_name = "user_detail/registeration_form.html"
     def form_valid(self, form):
        super(UserSignUp,self).form_valid(form)
        # The form is valid, automatically sign-in the user
        user = authenticate(self.request, username=form.cleaned_data['username'],
        password=form.cleaned_data['password1'])
        if user == None:
            # User not validated for some reason, return standard form_valid() response
            return self.render_to_response(self.get_context_data(form=form))
        else:
            # Log the user in
            login(self.request, user)
            # Redirect to success url
            return HttpResponseRedirect(self.get_success_url())



class UserUpdateForm(forms.ModelForm):

    class Meta:
        model=User
        fields=['first_name','last_name','mobile_number','email']

        widgets = {

            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'mobile_number': forms.TextInput(attrs={'placeholder': 'Mobile Number'}),
            'email': forms.TextInput(attrs={'placeholder': 'Email'}),

        }


