#-*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from snd.models import *
from datetimewidget.widgets import DateWidget
from coldeportes.utilities import adicionarClase

class DeportistaForm(ModelForm):
    fecha_nacimiento = forms.DateField(widget=forms.DateInput(format = '%Y-%m-%d'), input_formats=('%Y-%m-%d',))
    def __init__(self, *args, **kwargs):
        super(DeportistaForm, self).__init__(*args, **kwargs)
        self.fields['ciudad_residencia'] = adicionarClase(self.fields['ciudad_residencia'], 'one')
        self.fields['genero'] = adicionarClase(self.fields['genero'], 'one')
        self.fields['disciplinas'] = adicionarClase(self.fields['disciplinas'], 'many')
        self.fields['nacionalidad'] = adicionarClase(self.fields['nacionalidad'], 'many')
        self.fields['tipo_id'] = adicionarClase(self.fields['tipo_id'], 'one')
        self.fields['fecha_nacimiento'] = adicionarClase(self.fields['fecha_nacimiento'],'fecha')
        self.fields['etnia'] = adicionarClase(self.fields['etnia'], 'one')

    class Meta:
        model = Deportista
        exclude = ('entidad','estado',)

class ComposicionCorporalForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ComposicionCorporalForm, self).__init__(*args, **kwargs)
        self.fields['RH'] = adicionarClase(self.fields['RH'], 'one')
        self.fields['tipo_talla'] = adicionarClase(self.fields['tipo_talla'], 'one')

    class Meta:
        model = ComposicionCorporal
        exclude = ('deportista',)

class HistorialDeportivoForm(ModelForm):
    descripcion = forms.CharField(widget=forms.Textarea, required=False)
    def __init__(self, *args, **kwargs):
        super(HistorialDeportivoForm, self).__init__(*args, **kwargs)
        self.fields['tipo'] = adicionarClase(self.fields['tipo'], 'one')
        self.fields['fecha_inicial'] = adicionarClase(self.fields['fecha_inicial'], 'fecha')
        self.fields['fecha_final'] = adicionarClase(self.fields['fecha_final'], 'fecha')
        self.fields['descripcion'].widget.attrs['rows'] = 3

    def clean(self):
        fecha_comienzo = self.cleaned_data['fecha_inicial']
        fecha_fin = self.cleaned_data['fecha_final']
        if fecha_fin != None:
            if fecha_fin < fecha_comienzo:
                msg = "La fecha de finalización es menor a la fecha de comienzo"
                self.add_error('fecha_inicial', msg)
                self.add_error('fecha_final', msg)

    class Meta:
        model = HistorialDeportivo
        exclude = ('deportista',)

class InformacionAcademicaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(InformacionAcademicaForm, self).__init__(*args, **kwargs)
        self.fields['nivel'] = adicionarClase(self.fields['nivel'], 'one')
        self.fields['estado'] = adicionarClase(self.fields['estado'], 'one')
        self.fields['pais'] = adicionarClase(self.fields['pais'], 'one')

    class Meta:
        model = InformacionAcademica
        exclude = ('deportista',)
