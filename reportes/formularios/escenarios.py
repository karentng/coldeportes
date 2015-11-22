from django.forms import *
from django import forms
from entidades.models import Departamento, Ciudad, TipoDisciplinaDeportiva
from coldeportes.utilities import adicionarClase
from reportes.forms import add_visualizacion

class FiltrosEscenariosDMDForm(forms.Form):
    def __init__(self, *args, **kwargs):
        visualizaciones_definidas = kwargs.pop('visualizaciones', None)
        super(FiltrosEscenariosDMDForm, self).__init__(*args, **kwargs)
        self.fields['departamentos'] = adicionarClase(self.fields['departamentos'], 'many')
        self.fields['disciplinas'] = adicionarClase(self.fields['disciplinas'], 'many')
        self.fields['municipios'] = adicionarClase(self.fields['municipios'], 'many')
        self.fields['visualizacion'] = adicionarClase(self.fields['visualizacion'], 'one')


        add_visualizacion(self.fields['visualizacion'], visualizaciones_definidas)


    departamentos = forms.ModelMultipleChoiceField(queryset=Departamento.objects.all(), required=False)
    municipios = forms.ModelMultipleChoiceField(queryset=Ciudad.objects.all(), required=False)
    disciplinas = forms.ModelMultipleChoiceField(queryset=TipoDisciplinaDeportiva.objects.all().order_by('descripcion'), required=False, label="Disciplina Deportiva")
    visualizacion = forms.ChoiceField()