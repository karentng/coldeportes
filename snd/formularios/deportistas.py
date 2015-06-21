#-*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from snd.models import *
from datetimewidget.widgets import DateWidget
from snd.utilities import adicionarClase

class DeportistaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(DeportistaForm, self).__init__(*args, **kwargs)
        self.fields['ciudad_nacimiento'] = adicionarClase(self.fields['ciudad_nacimiento'], 'one')
        self.fields['genero'] = adicionarClase(self.fields['genero'], 'one')
        self.fields['disciplinas'] = adicionarClase(self.fields['disciplinas'], 'many')
        self.fields['nacionalidad'] = adicionarClase(self.fields['nacionalidad'], 'many')
        self.fields['tipo_id'] = adicionarClase(self.fields['tipo_id'], 'one')
        self.fields['fecha_nacimiento'] = adicionarClase(self.fields['fecha_nacimiento'],'fecha')

    class Meta:
        model = Deportista
        exclude = ('entidad','activo',)
        widgets = {
            'fecha_nacimiento': DateWidget(attrs={'id':"id_fecha_nacimiento"}, options={'format': 'yyyy-mm-dd'}, usel10n = True, bootstrap_version=3),

        }

class ComposicionCorporalForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ComposicionCorporalForm, self).__init__(*args, **kwargs)
        self.fields['RH'] = adicionarClase(self.fields['RH'], 'one')

    class Meta:
        model = ComposicionCorporal
        exclude = ('deportista',)

class HistorialDeportivoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(HistorialDeportivoForm, self).__init__(*args, **kwargs)
        self.fields['tipo'] = adicionarClase(self.fields['tipo'], 'one')
        self.fields['fecha'] = adicionarClase(self.fields['fecha'], 'fecha')

    class Meta:
        model = HistorialDeportivo
        exclude = ('deportista',)
        widgets = {
            'fecha': DateWidget(attrs={'id':"id_fecha"}, options={'format': 'yyyy-mm-dd'}, usel10n = True, bootstrap_version=3),

        }

class InformacionAcademicaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(InformacionAcademicaForm, self).__init__(*args, **kwargs)
        self.fields['nivel'] = adicionarClase(self.fields['nivel'], 'one')
        self.fields['estado'] = adicionarClase(self.fields['estado'], 'one')
        self.fields['pais'] = adicionarClase(self.fields['pais'], 'one')

    class Meta:
        model = InformacionAcademica
        exclude = ('deportista',)
