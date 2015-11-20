from django.forms import *
from django import forms
from entidades.models import Departamento, Ciudad, TipoDisciplinaDeportiva
from coldeportes.utilities import adicionarClase
from reportes.forms import add_visualizacion

class EstratoForm(forms.Form):
    def __init__(self, *args, **kwargs):
        visualizaciones_definidas = kwargs.pop('visualizaciones', None)
        super(EstratoForm, self).__init__(*args, **kwargs)
        self.fields['departamento'] = adicionarClase(self.fields['departamento'], 'many')
        self.fields['disciplina'] = adicionarClase(self.fields['disciplina'], 'many')
        self.fields['visualizacion'] = adicionarClase(self.fields['visualizacion'], 'one')
        self.fields['anno'] = adicionarClase(self.fields['anno'], 'many')

        add_visualizacion(self.fields['visualizacion'], visualizaciones_definidas)


    departamento = forms.ModelMultipleChoiceField(queryset=Departamento.objects.all(), required=False)
    disciplina = forms.ModelMultipleChoiceField(queryset=TipoDisciplinaDeportiva.objects.all(), required=False, label="disciplina deportiva")
    anno = forms.MultipleChoiceField(choices=((2013, 2013),(2014, 2014),(2015, 2015),),required=False, label="Año")
    visualizacion = forms.ChoiceField()


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
    disciplinas = forms.ModelMultipleChoiceField(queryset=TipoDisciplinaDeportiva.objects.all(), required=False, label="Disciplina Deportiva")
    visualizacion = forms.ChoiceField()