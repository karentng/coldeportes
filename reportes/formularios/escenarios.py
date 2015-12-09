from django.forms import *
from django import forms
from entidades.models import Departamento, Ciudad, TipoDisciplinaDeportiva
from coldeportes.utilities import adicionarClase
from reportes.forms import add_visualizacion

class FiltrosEscenariosDMDForm(forms.Form):
    
    TIPO_REPORTE = (
        ('CA', 'Clase de Acceso'),
        ('DT', 'División Territorial'),
        ('ES', 'Estrato'),
        ('EF', 'Estados Físicos'),
        ('TE', 'Tipo de Escenarios'),
        ('TS', 'Tipo de Superficie'),
        ('TP', 'Tipo de Propietario'),
    )
    def __init__(self, *args, **kwargs):
        visualizaciones_definidas = kwargs.pop('visualizaciones', None)
        eliminar = kwargs.pop('eliminar', None)
        super(FiltrosEscenariosDMDForm, self).__init__(*args, **kwargs)
        self.fields['departamentos'] = adicionarClase(self.fields['departamentos'], 'many')
        self.fields['disciplinas'] = adicionarClase(self.fields['disciplinas'], 'many')
        self.fields['municipios'] = adicionarClase(self.fields['municipios'], 'many')
        self.fields['visualizacion'] = adicionarClase(self.fields['visualizacion'], 'one')
        self.fields['reporte'] = adicionarClase(self.fields['reporte'], 'one')

        if eliminar:
            del self.fields[eliminar]


        add_visualizacion(self.fields['visualizacion'], visualizaciones_definidas)


    departamentos = forms.ModelMultipleChoiceField(queryset=Departamento.objects.all(), required=False)
    municipios = forms.ModelMultipleChoiceField(queryset=Ciudad.objects.all(), required=False)
    disciplinas = forms.ModelMultipleChoiceField(queryset=TipoDisciplinaDeportiva.objects.all().order_by('descripcion'), required=False, label="Disciplina Deportiva")
    reporte = forms.ChoiceField(label="Reporte",required=False,choices=TIPO_REPORTE)
    visualizacion = forms.ChoiceField()

