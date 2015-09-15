from django import forms
from django.forms import ModelForm
from normograma.models import *
from coldeportes.utilities import adicionarClase

class NormaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(NormaForm, self).__init__(*args, **kwargs)
        self.fields['sector'] = adicionarClase(self.fields['sector'], 'one')
        self.fields['descripcion'].widget.attrs['rows'] = 3
        self.fields['palabras_clave'].widget.attrs['rows'] = 3
    class Meta:
        model = Norma
        fields = '__all__'