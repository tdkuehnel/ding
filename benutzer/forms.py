from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from captcha.fields import CaptchaField

from benutzer.models import Benutzer

# Anmeldeform

class AnmeldeForm(AuthenticationForm):

    def clean_username(self):
        #import pdb; pdb.set_trace()
        data = self.cleaned_data['username']
        return data.lower()
