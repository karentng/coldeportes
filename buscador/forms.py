from django import forms

from entidades.modelos_vistas_reportes import PublicCafView
from entidades.models import Departamento, Ciudad
from coldeportes.utilities import adicionarClase

class BuscadorCafForm(forms.Form):
    nombre = forms.CharField(required=False)
    ciudades = forms.ModelMultipleChoiceField(queryset=Ciudad.objects.all(), required=False)
    departamentos = forms.ModelMultipleChoiceField(queryset=Departamento.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        super(BuscadorCafForm, self).__init__(*args, **kwargs)
        self.fields['departamentos'] = adicionarClase(self.fields['departamentos'], 'many')
        self.fields['ciudades'] = adicionarClase(self.fields['ciudades'], 'many')