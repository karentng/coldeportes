#-*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from snd.models import *
from entidades.models import CaracteristicaEscenario, Dias
from datetimewidget.widgets import TimeWidget, DateWidget, DateTimeWidget
from coldeportes.utilities import *

class CajaCompensacionForm(ModelForm):
    required_css_class = 'required'

    descripcion = forms.CharField(widget=forms.Textarea, required=False)
    def __init__(self, *args, **kwargs):
        super(CajaCompensacionForm, self).__init__(*args, **kwargs)
        self.fields['descripcion'].widget.attrs['rows'] = 3
        self.fields['clasificacion'] = adicionarClase(self.fields['clasificacion'], 'one')
        self.fields['region'] = adicionarClase(self.fields['region'], 'one')
        self.fields['publico'] = adicionarClase(self.fields['publico'], 'one')
        self.fields['infraestructura'] = adicionarClase(self.fields['infraestructura'], 'one')
        self.fields['tipo_institucion'] = adicionarClase(self.fields['tipo_institucion'], 'one')
        self.fields['estado'] = adicionarClase(self.fields['estado'], 'one')
        self.fields['ciudad'] = adicionarClase(self.fields['ciudad'], 'one')
        self.fields['servicios'] = adicionarClase(self.fields['servicios'], 'many')

    class Meta:
        model = CajaCompensacion
        exclude = ('entidad',)


class HorariosDisponibleCajasForm(ModelForm):
    required_css_class = 'required'

    hora_inicio = forms.TimeField(widget=TimeWidget(options={'format':'hh:ii'}))
    hora_fin = forms.TimeField(widget=TimeWidget(options={'format':'hh:ii'}))
    descripcion = forms.CharField(widget=forms.Textarea, required=True)

    def __init__(self, *args, **kwargs):
        super(HorariosDisponibleCajasForm, self).__init__(*args, **kwargs)
        self.fields['dias'] = adicionarClase(self.fields['dias'], 'many')
        self.fields['descripcion'].widget.attrs['rows'] = 3
        
    class Meta:

        model = HorarioDisponibilidadCajas
        exclude = ('caja_compensacion',)
        

class TarifaCajasForm(ModelForm):
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        super(TarifaCajasForm, self).__init__(*args, **kwargs)
        self.fields['descripcion'].widget.attrs['rows'] = 3
        
    class Meta:
        model = Tarifa
        exclude = ('caja_compensacion',)
