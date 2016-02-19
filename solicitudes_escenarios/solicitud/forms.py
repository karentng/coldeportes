#-*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from solicitudes_escenarios.solicitud.models import SolicitudEscenario,Escenario
from coldeportes.utilities import adicionarClase

class SolicitudEscenarioForm(ModelForm):
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        super(SolicitudEscenarioForm, self).__init__(*args, **kwargs)
        self.fields['escenarios'] = adicionarClase(self.fields['escenarios'], 'many')
        self.fields['tipo'] = adicionarClase(self.fields['tipo'], 'one')
        self.fields['prioridad'] = adicionarClase(self.fields['prioridad'], 'one')
        self.fields['para_quien'] = adicionarClase(self.fields['para_quien'], 'one')

    def clean(self):
        cleaned_data = super(SolicitudEscenarioForm, self).clean()
        return self.cleaned_data

    class Meta:
        model = SolicitudEscenario
        exclude = ('fecha',)