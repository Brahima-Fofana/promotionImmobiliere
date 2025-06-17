from xml.dom import ValidationErr

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelForm



class InscriptionForms(UserCreationForm):
    class Meta:
        model= User
        fields= ['username', 'email', 'password1', 'password2']

class UserInformationForm(forms.Form):
    nom = forms.CharField(max_length=255)
    prenom = forms.CharField(max_length=255)
    email = forms.EmailField()
    localisation = forms.CharField(max_length=255)
    cni = forms.CharField(max_length=255)
    poste = forms.CharField(max_length=255)
    contact1 = forms.CharField(max_length=20)
    contact2 = forms.CharField(max_length=20, required=False)

class PasswordOublierForm(forms.Form):
    username = forms.CharField(max_length=255)
    email = forms.EmailField()
    cni = forms.CharField(max_length=255)
    contact = forms.CharField(max_length=20)
