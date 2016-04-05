# -*- coding: utf-8 -*-
from django import forms
from snd.models import EscuelaDeportiva, Participante, Acudiente
from coldeportes.utilities import adicionarClase, verificar_tamano_archivo, MyDateWidget


class ParticipanteForm(forms.ModelForm):
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        super(ParticipanteForm, self).__init__(*args, **kwargs)
        self.fields['ciudad_residencia'] = adicionarClase(self.fields['ciudad_residencia'], 'one')
        self.fields['anho_curso'] = adicionarClase(self.fields['anho_curso'], 'one')
        self.fields['eps'] = adicionarClase(self.fields['eps'], 'one')
        self.fields['eps'].widget.attrs.update({'style': 'height: 71px;'})
        self.fields['nacionalidad'] = adicionarClase(self.fields['nacionalidad'], 'many')
        self.fields['etnia'] = adicionarClase(self.fields['etnia'], 'one')

    class Meta:
        model = Participante
        exclude = ('entidad', 'fecha_creacion', 'estado')

        widgets = {
            'fecha_nacimiento': MyDateWidget()
        }


class AcudienteForm(forms.ModelForm):
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        super(AcudienteForm, self).__init__(*args, **kwargs)
        self.fields['eps'] = adicionarClase(self.fields['eps'], 'one')
        self.fields['eps'].widget.attrs.update({'style': 'height: 71px;'})

    class Meta:
        model = Acudiente
        exclude = ('fecha_creacion', 'estado')

        widgets = {
            'fecha_nacimiento': MyDateWidget()
        }


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
        exclude = ('entidad', 'servicios', 'estado', 'fecha_creacion')


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