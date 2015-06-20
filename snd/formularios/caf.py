#-*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from snd.models import *
from snd.utilities import adicionarClase

class CentroAcondicionamientoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CentroAcondicionamientoForm, self).__init__(*args, **kwargs)
        self.fields['ciudad'] = adicionarClase(self.fields['ciudad'], 'one')
        self.fields['contacto'].widget.attrs['rows'] = 3

    class Meta:
        model = CentroAcondicionamiento
        exclude = ('entidad', 'activo',)

class CACostoUsoForm(ModelForm):
    class Meta:
        model = CACostoUso
        exclude = ('centro', 'libre',)

    def save(self, commit=True):
        instance = super(CACostoUsoForm, self).save(commit=False)
        if instance.privado == 0 and instance.publico == 0:
            instance.libre = True
        else:
            instance.libre = False
        if commit:
            instance.save()
        return instance

class CAServiciosForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CAServiciosForm, self).__init__(*args, **kwargs)
        self.fields['acondicionamiento'].widget.attrs = {'data-render':'switchery'}
        self.fields['fortalecimiento'].widget.attrs = {'data-render':'switchery',}
        self.fields['zona_cardio'].widget.attrs = {'data-render':'switchery',}
        self.fields['zona_humeda'].widget.attrs = {'data-render':'switchery',}
        self.fields['medico'].widget.attrs = {'data-render':'switchery',}
        self.fields['nutricionista'].widget.attrs = {'data-render':'switchery',}
        self.fields['fisioterapia'].widget.attrs = {'data-render':'switchery',}

    class Meta:
        model = CAServicios
        exclude = ('centro',)
        widget = {
            'acondicionamiento': forms.CheckboxInput(),
        }

class CAOtrosForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CAOtrosForm, self).__init__(*args, **kwargs)
        self.fields['camerinos'].widget.attrs = {'data-render':'switchery'}
        self.fields['duchas'].widget.attrs = {'data-render':'switchery',}
        self.fields['comentarios'].widget.attrs['rows'] = 3
    
    class Meta:
        model = CAOtros
        exclude = ('centro',)