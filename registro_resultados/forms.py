# -*- encoding: utf-8 -*-
from django import forms
from registro_resultados.models import *
from coldeportes.utilities import adicionarClase

class CompetenciaForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CompetenciaForm, self).__init__(*args, **kwargs)
        self.fields['categorias'] = adicionarClase(self.fields['categorias'], 'many')

    class Meta:
        model = Competencia
        exclude = ()

class ParticipanteForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        competencia = kwargs.pop('competencia')
        super(ParticipanteForm, self).__init__(*args, **kwargs)
        self.fields['departamento'] = adicionarClase(self.fields['departamento'], 'one')
        if competencia.tiempos != True:
            del self.fields['tiempo']

        if competencia.tipos_participantes == 1:
            del self.fields['equipo']

    class Meta:
        model = Participante
        exclude = ("competencia",)

class EquipoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EquipoForm, self).__init__(*args, **kwargs)
        self.fields['departamento'] = adicionarClase(self.fields['departamento'], 'one')

    class Meta:
        model = Equipo
        exclude = ("competencia",)