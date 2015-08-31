#-*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from snd.models import *
import datetime
from coldeportes.utilities import adicionarClase

class SeleccionForm(ModelForm):
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        super(SeleccionForm, self).__init__(*args, **kwargs)
        self.fields['tipo'] = adicionarClase(self.fields['tipo'], 'one')
        self.fields['tipo_campeonato'] = adicionarClase(self.fields['tipo_campeonato'], 'one')
        self.fields['fecha_inicial'] = adicionarClase(self.fields['fecha_inicial'],'fecha')
        self.fields['fecha_final'] = adicionarClase(self.fields['fecha_final'],'fecha')

    class Meta:
        model = Seleccion
        exclude = ('deportistas','personal_apoyo',)