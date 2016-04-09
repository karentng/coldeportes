#-*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from coldeportes.utilities import adicionarClase, verificar_tamano_archivo
from entidades.models import Entidad
from reconocimiento_deportivo.modelos.solicitudes import ReconocimientoDeportivo#, AdjuntoSolicitud, DiscucionReconocimiento

class ReconocimientoDeportivoForm(ModelForm):
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        super(ReconocimientoDeportivoForm, self).__init__(*args, **kwargs)
        self.fields['para_quien'] = adicionarClase(self.fields['para_quien'], 'one')
        self.fields['vinculo_solicitante'] = adicionarClase(self.fields['vinculo_solicitante'], 'one')
        self.fields['tipo'] = adicionarClase(self.fields['tipo'], 'one')
        self.fields['descripcion'].widget.attrs['rows'] = 3
        self.fields['para_quien'].queryset = Entidad.objects.filter(tipo=5)

    class Meta:
        model = ReconocimientoDeportivo
        exclude = ('fecha_creacion','estado', 'fecha_vigencia')
