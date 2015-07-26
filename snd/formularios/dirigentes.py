from django import forms
from django.forms import ModelForm
from snd.models import *
from datetimewidget.widgets import DateWidget
from coldeportes.utilities import adicionarClase


class DirigenteForm(ModelForm):

    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        super(DirigenteForm, self).__init__(*args, **kwargs)
        self.fields['superior'] = adicionarClase(self.fields['superior'], 'one')
        self.fields['nacionalidad'] = adicionarClase(self.fields['nacionalidad'], 'many')
        self.fields['fecha_retiro'] = adicionarClase(self.fields['fecha_retiro'], 'fecha')
        self.fields['fecha_posesion'] = adicionarClase(self.fields['fecha_posesion'], 'fecha')
        self.fields['ciudad_residencia'] = adicionarClase(self.fields['ciudad_residencia'], 'one')


    class Meta:
        model = Dirigente
        #fields = '__all__'
        exclude = ('entidad', 'estado',)

class DirigenteFuncionesForm(ModelForm):

    required_css_class = 'required'
    
    class Meta:
        model = Funcion
        exclude = ('dirigente',)