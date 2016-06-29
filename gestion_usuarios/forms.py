# -*- encoding: utf-8 -*-
from django import forms
from django.contrib.auth.models import *
from django.contrib.auth.forms import UserCreationForm
from snd.formularios.caf import adicionarClase
from gestion_usuarios.models import PERMISOS_DIGITADOR
from coldeportes.utilities import permisosPermitidos


class UserForm(UserCreationForm):
    required_css_class = 'required'
    grupo = forms.ModelChoiceField(queryset=Group.objects.all())

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['grupo'] = adicionarClase(self.fields['grupo'], 'one')
        self.fields['password2'].help_text = 'Introduzca nuevamente la contraseña, para verificación'

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'grupo',)


class UserModificarForm(forms.ModelForm):
    required_css_class = 'required'
    grupo = forms.ModelChoiceField(queryset=Group.objects.all())

    def __init__(self, *args, **kwargs):
        super(UserModificarForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'grupo',)
        exclude = ('password1', 'password2',)


class UserPasswordForm(forms.Form):
    required_css_class = 'required'
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password (Confirmación)", widget=forms.PasswordInput)


class GroupForm(forms.ModelForm):
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        instancia = kwargs.get('instance', None)
        super(GroupForm, self).__init__(*args, **kwargs)
        self.fields['permissions'].queryset = self.fields['permissions'].queryset.filter(codename__in=permisosPermitidos(request, PERMISOS_DIGITADOR))
        self.fields['permissions'] = adicionarClase(self.fields['permissions'], 'many')

        if instancia != None:
            # evitar que editen los nombres de los grupos por defecto, podrian dejar de funcionar algunas cosas
            if instancia.name == 'Solo lectura' or instancia.name == 'Digitador':
                self.fields['name'].widget.attrs['readonly'] = True

    class Meta:
        model = Group
        exclude = ()