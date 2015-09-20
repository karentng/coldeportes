#-*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from normograma.models import *
from coldeportes.utilities import adicionarClase
from django.forms.extras.widgets import SelectDateWidget

SECTORES = (
        ('D', 'Deporte'),
        ('E', 'Educación Física'),
        ('R', 'Recreación'),
    )
class NormaForm(forms.ModelForm):
    required_css_class = 'required'

    sector = forms.MultipleChoiceField(label="Sector", widget=forms.SelectMultiple(attrs={'placeholder': 'Sector'}), choices=SECTORES)

    def __init__(self, *args, **kwargs):
        super(NormaForm, self).__init__(*args, **kwargs)
        self.fields['sector'] = adicionarClase(self.fields['sector'], 'many')
        self.fields['año'] = adicionarClase(self.fields['año'], 'one')
        self.fields['jurisdiccion'] = adicionarClase(self.fields['jurisdiccion'], 'one')
        self.fields['descripcion'].widget.attrs['rows'] = 3
        self.fields['palabras_clave'].widget.attrs['rows'] = 3
    class Meta:
        model = Norma
        fields = '__all__'

class NormogramaBusquedaForm(forms.Form):

    texto_a_buscar = forms.CharField(required=False, label="Búsqueda", widget=forms.TextInput(attrs={'placeholder': 'Ingrese úna búsqueda'}))
    sector = forms.MultipleChoiceField(label="Sector", required=False, widget=forms.SelectMultiple(attrs={'placeholder': 'Sector'}), choices=SECTORES)

    def __init__(self, *args, **kwargs):
        super(NormogramaBusquedaForm, self).__init__(*args, **kwargs)
        self.fields['sector'] = adicionarClase(self.fields['sector'], 'many')
