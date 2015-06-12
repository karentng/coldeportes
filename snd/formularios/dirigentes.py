from django import forms
from django.forms import ModelForm
from snd.models import *

def adicionarClase(campo, clase):
    campo.widget.attrs.update({'class': clase})
    return campo

class DirigenteForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(DirigenteForm, self).__init__(*args, **kwargs)
        self.fields['superior'] = adicionarClase(self.fields['superior'], 'one')

    class Meta:
        model = Dirigente
        #fields = '__all__'
        exclude = ('entidad','activo',)

class DirigenteFuncionesForm(ModelForm):
    class Meta:
        model = Funcion
        exclude = ('dirigente',)