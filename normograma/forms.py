#-*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from normograma.models import *
from coldeportes.utilities import adicionarClase
from django.forms.extras.widgets import SelectDateWidget


class NormaForm(forms.ModelForm):
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        super(NormaForm, self).__init__(*args, **kwargs)
        self.fields['sectores'] = adicionarClase(self.fields['sectores'], 'many')
        self.fields['anio'] = adicionarClase(self.fields['anio'], 'one')
        self.fields['jurisdiccion'] = adicionarClase(self.fields['jurisdiccion'], 'one')
        self.fields['descripcion'].widget.attrs['rows'] = 3
        self.fields['palabras_clave'].widget.attrs['rows'] = 3

    class Meta:
        model = Norma
        fields = '__all__'



class NormogramaBusquedaForm(forms.Form):
    JURISDICCIONES = (('D', 'Departamental'), ('M', 'Municipal'), ('N', 'Nacional'))

    texto_a_buscar = forms.CharField(required=False, label="Título de Norma / Palabras Clave / Año", widget=forms.TextInput(attrs={'placeholder': 'Ingrese nombre de norma, año y/o palabras claves'}))
    sector = forms.MultipleChoiceField(label="Sector", required=False, widget=forms.SelectMultiple(attrs={'placeholder': 'Sector'}))
    jurisdiccion = forms.MultipleChoiceField(label="Jurisdicción", required=False, widget=forms.SelectMultiple(attrs={'placeholder': 'Jurisdicción'}), choices=JURISDICCIONES)
    #anio = forms.MultipleChoiceField(label="Año", required=False, widget=forms.SelectMultiple(attrs={'placeholder': 'Año'}), choices=ANIOS)

    def __init__(self, *args, **kwargs):
        super(NormogramaBusquedaForm, self).__init__(*args, **kwargs)
        self.fields['sector'] = adicionarClase(self.fields['sector'], 'many')
        self.fields['jurisdiccion'] = adicionarClase(self.fields['jurisdiccion'], 'many')
        #self.fields['anio'] = adicionarClase(self.fields['anio'], 'many')
