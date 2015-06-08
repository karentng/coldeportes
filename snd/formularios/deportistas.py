#-*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from snd.models import *
from datetimewidget.widgets import DateWidget

def adicionarClase(campo, clase):
    campo.widget.attrs.update({'class': clase})
    return campo

class DeportistaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(DeportistaForm, self).__init__(*args, **kwargs)
        self.fields['ciudad_nacimiento'] = adicionarClase(self.fields['ciudad_nacimiento'], 'one')
        self.fields['sexo'] = adicionarClase(self.fields['sexo'], 'one')
        self.fields['disciplinas'] = adicionarClase(self.fields['disciplinas'], 'many')
        self.fields['nacionalidad'] = adicionarClase(self.fields['nacionalidad'], 'many')

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
        widgets = {
            'fecha_finalizacion': DateWidget(attrs={'id':"id_fecha_finalizacion"}, options={'format': 'yyyy-mm-dd'}, usel10n = True, bootstrap_version=3),
            'fecha_desercion': DateWidget(attrs={'id':"id_fecha_desercion"}, options={'format': 'yyyy-mm-dd'}, usel10n = True, bootstrap_version=3),

        }
