#-*- coding: utf-8 -*-
from django import forms
from snd.models import *
from coldeportes.utilities import adicionarClase, verificar_tamano_archivo

class CentroAcondicionamientoForm(forms.ModelForm):
    required_css_class = 'required'
    def __init__(self, *args, **kwargs):
        super(CentroAcondicionamientoForm, self).__init__(*args, **kwargs)
        self.fields['ciudad'] = adicionarClase(self.fields['ciudad'], 'one')
        self.fields['estrato'] = adicionarClase(self.fields['estrato'], 'one')

    class Meta:
        model = CentroAcondicionamiento
        exclude = ('entidad', 'clases', 'servicios', 'estado',)

class CAPlanForm(forms.ModelForm):
    required_css_class = 'required'
    def __init__(self, *args, **kwargs):
        super(CAPlanForm, self).__init__(*args, **kwargs)
        self.fields['descripcion'].widget.attrs['rows'] = 3
    class Meta:
        model = CAPlan
        exclude = ('centro',)

class CAClasesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CAClasesForm, self).__init__(*args, **kwargs)
        self.fields['clases'] = adicionarClase(self.fields['clases'], 'styled')
        self.fields['clases'].queryset = self.fields['clases'].queryset.order_by('nombre')
    class Meta:
        model = CentroAcondicionamiento
        fields = ('clases',)
        widgets = {
            'clases': forms.CheckboxSelectMultiple
        }

class CAServiciosForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CAServiciosForm, self).__init__(*args, **kwargs)
        self.fields['servicios'] = adicionarClase(self.fields['servicios'], 'styled')
        self.fields['servicios'].queryset = self.fields['servicios'].queryset.order_by('nombre')
    class Meta:
        model = CentroAcondicionamiento
        fields = ('servicios',)
        widgets = {
            'servicios': forms.CheckboxSelectMultiple
        }

class CAFotoForm(forms.ModelForm):
    required_css_class = 'required'

    def clean(self):
        cleaned_data = super(CAFotoForm, self).clean()
        self = verificar_tamano_archivo(self, cleaned_data, "foto")
        return self.cleaned_data

    class Meta:
        model = CAFoto
        exclude = ('centro',)