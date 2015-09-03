#-*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from snd.models import *
import datetime
from coldeportes.utilities import adicionarClase,MyDateWidget

class VerificarExistenciaForm(forms.Form):
    TIPO_IDENTIDAD = (
        ('CC', 'CÉDULA DE CIUDADANÍA'),
        ('TI', 'TARJETA DE IDENTIDAD'),
        ('CE', 'CÉDULA DE EXTRANJERÍA'),
        ('PS', 'PASAPORTE'),
    )
    tipo_id = forms.ChoiceField(label='Tipo de documento',choices=TIPO_IDENTIDAD)
    identificacion = forms.IntegerField(label="Identificación del deportista")

class CambioDocumentoForm(ModelForm):
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        super(CambioDocumentoForm, self).__init__(*args, **kwargs)
        self.fields['tipo_documento_nuevo'] = adicionarClase(self.fields['tipo_documento_nuevo'], 'one')
        self.fields['tipo_documento_anterior'].widget.attrs.update({'readonly': True})
        self.fields['identificacion_anterior'].widget.attrs.update({'readonly': True})
        self.fields['tipo_documento_anterior'].widget.attrs.update({'form': 'form-cambio-documento'})
        self.fields['identificacion_anterior'].widget.attrs.update({'form': 'form-cambio-documento'})

    class Meta:
        model = CambioDocumentoDeportista
        exclude = ('deportista',)

class DeportistaForm(ModelForm):
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        super(DeportistaForm, self).__init__(*args, **kwargs)
        self.fields['ciudad_residencia'] = adicionarClase(self.fields['ciudad_residencia'], 'one')
        self.fields['genero'] = adicionarClase(self.fields['genero'], 'one')
        self.fields['disciplinas'] = adicionarClase(self.fields['disciplinas'], 'many')
        self.fields['nacionalidad'] = adicionarClase(self.fields['nacionalidad'], 'many')
        self.fields['etnia'] = adicionarClase(self.fields['etnia'], 'one')
        self.fields['tipo_id'].widget.attrs.update({'readonly': True})
        self.fields['identificacion'].widget.attrs.update({'readonly': True})

    def clean(self):
        fecha_nacimiento = self.cleaned_data['fecha_nacimiento']
        if fecha_nacimiento > datetime.date.today():
                msg = "La fecha de nacimiento no puede ser mayor al día de hoy"
                self.add_error('fecha_nacimiento', msg)

    class Meta:
        model = Deportista
        exclude = ('entidad','estado',)
        widgets = {
            'fecha_nacimiento': MyDateWidget(),
        }

class ComposicionCorporalForm(ModelForm):

    required_css_class = 'required'
    is_mujer = None

    def __init__(self,is_mujer ,*args, **kwargs):
        super(ComposicionCorporalForm, self).__init__(*args, **kwargs)
        self.is_mujer = is_mujer
        self.fields['RH'] = adicionarClase(self.fields['RH'], 'one')
        self.fields['tipo_talla'] = adicionarClase(self.fields['tipo_talla'], 'one')
        self.fields['talla_camisa'] = adicionarClase(self.fields['talla_camisa'], 'one')
        self.fields['talla_pantaloneta'] = adicionarClase(self.fields['talla_pantaloneta'], 'one')
        self.fields['talla_zapato'] = adicionarClase(self.fields['talla_zapato'], 'one')
        self.fields['eps'] = adicionarClase(self.fields['eps'], 'one')
        self.fields['imc'].widget.attrs['readonly'] = 1
        self.fields['masa_corporal_magra'].widget.attrs['readonly'] = 1

    def clean(self):
        porcentaje_grasa = self.cleaned_data['porcentaje_grasa']
        if self.is_mujer:
            if porcentaje_grasa<8 or porcentaje_grasa>40:
                msg = 'Por favor ingrese datos reales'
                self.add_error('porcentaje_grasa',msg)
        else:
            if porcentaje_grasa<6  or porcentaje_grasa>35:
                msg = 'Por favor ingrese datos reales'
                self.add_error('porcentaje_grasa',msg)

    class Meta:
        model = ComposicionCorporal
        exclude = ('deportista',)
        widgets = {
            'fecha_inicia_deporte': MyDateWidget(),
        }


class HistorialDeportivoForm(ModelForm):

    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        super(HistorialDeportivoForm, self).__init__(*args, **kwargs)
        self.fields['tipo'] = adicionarClase(self.fields['tipo'], 'one')
        self.fields['pais'] = adicionarClase(self.fields['pais'], 'one')

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
        exclude = ('deportista','estado')
        widgets = {
            'fecha_inicial': MyDateWidget(),
            'fecha_final': MyDateWidget(),
        }

class InformacionAcademicaForm(ModelForm):

    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        super(InformacionAcademicaForm, self).__init__(*args, **kwargs)
        self.fields['nivel'] = adicionarClase(self.fields['nivel'], 'one')
        self.fields['estado'] = adicionarClase(self.fields['estado'], 'one')
        self.fields['pais'] = adicionarClase(self.fields['pais'], 'one')

    class Meta:
        model = InformacionAcademica
        exclude = ('deportista',)

#Formularios para transferencias
class DeportistaTransfer(ModelForm):
    class Meta:
        model = Deportista
        exclude = ('entidad','estado',)