# -*- encoding: utf-8 -*-
from django import forms
from django.contrib.auth.models import *
from django.contrib.auth.forms import UserCreationForm

class UserForm(UserCreationForm):
    grupo = forms.ModelChoiceField(queryset=Group.objects.all())
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'grupo',)

class UserModificarForm(forms.ModelForm):
    grupo = forms.ModelChoiceField(queryset=Group.objects.all())
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'grupo',)
        exclude = ('password1', 'password2',)

class UserPasswordForm(forms.Form):
	password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
	password2 = forms.CharField(label="Password (Confirmación)", widget=forms.PasswordInput)