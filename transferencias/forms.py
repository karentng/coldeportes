#-*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from snd.utilities import adicionarClase
from .models import Transferencia

class TransferenciaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(TransferenciaForm, self).__init__(*args, **kwargs)
        self.fields['entidad'] = adicionarClase(self.fields['entidad'], 'one')

    class Meta:
        model = Transferencia
        exclude = ('id_objeto','tipo_objeto','fecha_solicitud',)