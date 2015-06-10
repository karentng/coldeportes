from django import forms
from django.forms import ModelForm
from snd.models import *

def adicionarClase(campo, clase):
    campo.widget.attrs.update({'class': clase})
    return campo

class CrearDirigenteForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CrearDirigenteForm, self).__init__(*args, **kwargs)
        self.fields['superior'] = adicionarClase(self.fields['superior'], 'one')

    class Meta:
        model = Dirigente
        #fields = '__all__'
        exclude = ('entidad',)