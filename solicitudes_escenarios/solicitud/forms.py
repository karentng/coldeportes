#-*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from solicitudes_escenarios.solicitud.models import SolicitudEscenario,Escenario,AdjuntoSolicitud
from coldeportes.utilities import adicionarClase,verificar_tamano_archivo
from entidades.models import Entidad

class SolicitudEscenarioForm(ModelForm):
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        super(SolicitudEscenarioForm, self).__init__(*args, **kwargs)
        self.fields['escenarios'] = adicionarClase(self.fields['escenarios'], 'many')
        self.fields['prioridad'] = adicionarClase(self.fields['prioridad'], 'one')
        self.fields['para_quien'] = adicionarClase(self.fields['para_quien'], 'one')
        self.fields['descripcion'].widget.attrs['rows'] = 3
        self.fields['para_quien'].queryset = Entidad.objects.filter(tipo__in=[0,5])

    class Meta:
        model = SolicitudEscenario
        exclude = ('fecha','estado',)

class AdjuntoSolicitudForm(ModelForm):
    required_css_class = 'required'

    class Meta:
        model = AdjuntoSolicitud
        exclude = ('solicitud','discucion',)
