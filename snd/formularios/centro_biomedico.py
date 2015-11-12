#-*- coding: utf-8 -*-
from django import forms
from snd.models import CentroBiomedico
from coldeportes.utilities import adicionarClase

class CentroBiomedicoForm(forms.ModelForm):
    required_css_class = 'required'
    def __init__(self, *args, **kwargs):
        super(CentroBiomedicoForm, self).__init__(*args, **kwargs)
        self.fields['ciudad'] = adicionarClase(self.fields['ciudad'], 'one')
        self.fields['estrato'] = adicionarClase(self.fields['estrato'], 'one')

    class Meta:
        model = CentroBiomedico
        exclude = ('entidad','servicios','estado','fecha_creacion')

class CentroBiomedicoServiciosForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CentroBiomedicoServiciosForm, self).__init__(*args, **kwargs)
        self.fields['servicios'] = adicionarClase(self.fields['servicios'], 'styled')
        self.fields['servicios'].queryset = self.fields['servicios'].queryset.order_by('nombre')
    
    class Meta:
        model = CentroBiomedico
        fields = ('servicios',)
        widgets = {
            'servicios': forms.CheckboxSelectMultiple
        }