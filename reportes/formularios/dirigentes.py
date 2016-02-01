from django import forms
from entidades.models import Departamento, Ciudad
from coldeportes.utilities import adicionarClase
from reportes.forms import add_visualizacion

class NacionalidadForm(forms.Form):
    def __init__(self, *args, **kwargs):
        visualizaciones_definidas = kwargs.pop('visualizaciones', None)
        super(NacionalidadForm, self).__init__(*args, **kwargs)
        self.fields['departamentos'] = adicionarClase(self.fields['departamentos'], 'many')
        self.fields['genero'] = adicionarClase(self.fields['genero'], 'many')
        self.fields['visualizacion'] = adicionarClase(self.fields['visualizacion'], 'one')

        add_visualizacion(self.fields['visualizacion'], visualizaciones_definidas)

    departamentos = forms.ModelMultipleChoiceField(queryset=Departamento.objects.all(), required=False)
    genero = forms.MultipleChoiceField(choices=(('HOMBRE','MASCULINO'),('MUJER','FEMENINO'),), required=False, label="Género")
    visualizacion = forms.ChoiceField()