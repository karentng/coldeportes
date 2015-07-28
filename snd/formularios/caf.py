#-*- coding: utf-8 -*-
from django import forms
from snd.models import *
from coldeportes.utilities import adicionarClase

class CentroAcondicionamientoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CentroAcondicionamientoForm, self).__init__(*args, **kwargs)
        self.fields['ciudad'] = adicionarClase(self.fields['ciudad'], 'one')

    class Meta:
        model = CentroAcondicionamiento
        exclude = ('entidad', 'clases', 'servicios',)

class CAPlanForm(forms.ModelForm):
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
    class Meta:
        model = CAFoto
        exclude = ('centro',)

'''
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
'''