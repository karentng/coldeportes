from django import forms
from django.forms import ModelForm
from snd.models import *
from datetimewidget.widgets import DateWidget
from snd.utilities import adicionarClase


class DirigenteForm(ModelForm):

    descripcion = forms.CharField(widget=forms.Textarea, required=True)

    def __init__(self, *args, **kwargs):
        super(DirigenteForm, self).__init__(*args, **kwargs)
        self.fields['superior'] = adicionarClase(self.fields['superior'], 'one')
        self.fields['nacionalidad'] = adicionarClase(self.fields['nacionalidad'], 'many')
        self.fields['fecha_posesion'] = adicionarClase(self.fields['fecha_posesion'], 'fecha')
        self.fields['fecha_retiro'] = adicionarClase(self.fields['fecha_retiro'], 'fecha')

    class Meta:
        model = Dirigente
        #fields = '__all__'
        exclude = ('entidad','activo',)

class DirigenteFuncionesForm(ModelForm):

    descripcion = forms.CharField(widget=forms.Textarea, required=True)
    
    class Meta:
        model = Funcion
        exclude = ('dirigente',)