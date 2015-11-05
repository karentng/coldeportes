#-*- coding: utf-8 -*-
from django import forms
from snd.models import EscuelaDeportiva
from coldeportes.utilities import adicionarClase, verificar_tamano_archivo

class EscuelaDeportivaForm(forms.ModelForm):
    required_css_class = 'required'
    def __init__(self, *args, **kwargs):
        super(EscuelaDeportivaForm, self).__init__(*args, **kwargs)
        self.fields['ciudad'] = adicionarClase(self.fields['ciudad'], 'one')
        self.fields['estrato'] = adicionarClase(self.fields['estrato'], 'one')

    def clean(self):
        cleaned_data = super(EscuelaDeportivaForm, self).clean()
        self = verificar_tamano_archivo(self, cleaned_data, "aval")
        return self.cleaned_data

    class Meta:
        model = EscuelaDeportiva
        exclude = ('entidad','servicios','estado','fecha_creacion')

class EscuelaDeportivaServiciosForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EscuelaDeportivaServiciosForm, self).__init__(*args, **kwargs)
        self.fields['servicios'] = adicionarClase(self.fields['servicios'], 'styled')
        self.fields['servicios'].queryset = self.fields['servicios'].queryset.order_by('nombre')
    
    class Meta:
        model = EscuelaDeportiva
        fields = ('servicios',)
        widgets = {
            'servicios': forms.CheckboxSelectMultiple
        }