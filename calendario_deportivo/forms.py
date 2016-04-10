#-*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from coldeportes.utilities import adicionarClase,MyDateTimeWidget
from entidades.models import Entidad,CalendarioNacional

class CalendarioForm(ModelForm):
    required_css_class = 'required'
    def __init__(self, *args, **kwargs):
        super(CalendarioForm, self).__init__(*args, **kwargs)
        self.fields['tipo'] = adicionarClase(self.fields['tipo'], 'one')
        self.fields['ciudad'] = adicionarClase(self.fields['ciudad'], 'one')
        self.fields['modalidad'] = adicionarClase(self.fields['modalidad'], 'one')
        self.fields['categoria'] = adicionarClase(self.fields['categoria'], 'one')
        self.fields['deporte'] = adicionarClase(self.fields['deporte'], 'one')

    class Meta:
        model = CalendarioNacional
        exclude = ('estado','entidad',)
        widgets = {
            'fecha_inicio': MyDateTimeWidget(),
            'fecha_finalizacion': MyDateTimeWidget(),
            'fecha_inicio_preinscripcion': MyDateTimeWidget(),
            'fecha_finalizacion_preinscripcion': MyDateTimeWidget()
        }