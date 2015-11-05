from django.forms import *
from django import forms
from entidades.models import Departamento
from coldeportes.utilities import adicionarClase

VISUALIZACIONES = (
    (1, "Dona"),
    (2, "Comparativa Horizontal"),
    (3, "Comparativa Vertical"),
    (4, "Tree Map"), 
)

class DemografiaForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(DemografiaForm, self).__init__(*args, **kwargs)
        self.fields['departamento'] = adicionarClase(self.fields['departamento'], 'many')
        self.fields['visualizacion'] = adicionarClase(self.fields['visualizacion'], 'one')
        self.fields['anno'] = adicionarClase(self.fields['anno'], 'many')


    departamento = forms.ModelMultipleChoiceField(queryset=Departamento.objects.all(), required=False)
    anno = forms.MultipleChoiceField(choices=((2013, 2013),(2014, 2014),(2015, 2015),),required=False, label="Año")
    visualizacion = forms.ChoiceField(choices=VISUALIZACIONES)
