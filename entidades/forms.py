# -*- encoding: utf-8 -*-
from django.forms import *
from django import forms
from entidades.models import *
from coldeportes.utilities import adicionarClase

class EntidadForm(forms.ModelForm):
    pagina = forms.CharField(label="Página Web")

    def __init__(self, *args, **kwargs):
        super(EntidadForm, self).__init__(*args, **kwargs)
        self.fields['pagina'] = adicionarClase(self.fields['pagina'], 'form-control')

    class Meta:
        model = Entidad
        fields = ('nombre',)

class ActoresForm(forms.ModelForm):
    class Meta:
        model = Actores
        exclude = ()