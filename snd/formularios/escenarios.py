#-*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from snd.models import *
from entidades.models import CaracteristicaEscenario, Dias
from datetimewidget.widgets import TimeWidget, DateWidget
from coldeportes.utilities import adicionarClase


class IdentificacionForm(forms.ModelForm):
    required_css_class = 'required'

    descripcion = forms.CharField(widget=forms.Textarea, required=False, label="Descripción")
    def __init__(self, *args, **kwargs):
        super(IdentificacionForm, self).__init__(*args, **kwargs)
        self.fields['ciudad'] = adicionarClase(self.fields['ciudad'], 'one')
        self.fields['estado'] = adicionarClase(self.fields['estado'], 'one')
        self.fields['estrato'] = adicionarClase(self.fields['estrato'], 'one')
        self.fields['descripcion'].widget.attrs['rows'] = 3

    class Meta:
        model = Escenario
        exclude = ('entidad',)

class CaracterizacionForm(forms.ModelForm):
    required_css_class = 'required'

    descripcion = forms.CharField(widget=forms.Textarea, required=False)

    def __init__(self, *args, **kwargs):
        super(CaracterizacionForm, self).__init__(*args, **kwargs)
        self.fields['tipo_escenario'] = adicionarClase(self.fields['tipo_escenario'], 'one')
        self.fields['clase_acceso'] = adicionarClase(self.fields['clase_acceso'], 'one')
        self.fields['tipo_escenario'].queryset = TipoEscenario.objects.all().order_by('descripcion')
        self.fields['tipo_disciplinas'] = adicionarClase(self.fields['tipo_disciplinas'], 'many')
        self.fields['tipo_disciplinas'].queryset = TipoDisciplinaDeportiva.objects.all().order_by('descripcion')
        self.fields['tipo_superficie_juego'] = adicionarClase(self.fields['tipo_superficie_juego'], 'many')
        self.fields['tipo_superficie_juego'].queryset = TipoSuperficie.objects.all().order_by('descripcion')
        self.fields['caracteristicas'] = adicionarClase(self.fields['caracteristicas'], 'many')
        self.fields['caracteristicas'].queryset = CaracteristicaEscenario.objects.all().order_by('descripcion')
        self.fields['clase_uso'] = adicionarClase(self.fields['clase_uso'], 'many')
        self.fields['clase_uso'].queryset = TipoUsoEscenario.objects.all().order_by('descripcion')
        self.fields['descripcion'].widget.attrs['rows'] = 3
    class Meta:
        model = CaracterizacionEscenario
        exclude = ('escenario',)        
        

class HorariosDisponibleForm(ModelForm):
    required_css_class = 'required'

    descripcion = forms.CharField(widget=forms.Textarea, required=True)

    def __init__(self, *args, **kwargs):
        super(HorariosDisponibleForm, self).__init__(*args, **kwargs)
        self.fields['dias'] = adicionarClase(self.fields['dias'], 'many')
        self.fields['descripcion'].widget.attrs['rows'] = 3
        
    class Meta:

        model = HorarioDisponibilidad
        exclude = ('escenario',)
        widgets = {
            'hora_inicio': TimeWidget(attrs={'id':"id_hora_inicio"}, usel10n = True, bootstrap_version=3),
            'hora_fin': TimeWidget(attrs={'id':"id_hora_fin"}, usel10n = True, bootstrap_version=3)
        }

class DatoHistoricoForm(ModelForm):
    required_css_class = 'required'

    descripcion = forms.CharField(widget=forms.Textarea, required=True)
    
    def __init__(self, *args, **kwargs):
        super(DatoHistoricoForm, self).__init__(*args, **kwargs)
        self.fields['descripcion'].widget.attrs['rows'] = 3
        self.fields['fecha_inicio'] = adicionarClase(self.fields['fecha_inicio'], 'fecha')
        self.fields['fecha_fin'] = adicionarClase(self.fields['fecha_fin'], 'fecha')

    class Meta:
        model = DatoHistorico
        exclude = ('escenario',)
        

class FotoEscenarioForm(ModelForm):
    required_css_class = 'required'

    class Meta:
        model = Foto
        exclude = ('escenario',)

class VideoEscenarioForm(ModelForm):
    required_css_class = 'required'

    class Meta:
        model = Video
        exclude = ('escenario',)

class ContactoForm(ModelForm):
    required_css_class = 'required'
    
    descripcion = forms.CharField(widget=forms.Textarea, required=True)

    def __init__(self, *args, **kwargs):
        super(ContactoForm, self).__init__(*args, **kwargs)
        self.fields['descripcion'].widget.attrs['rows'] = 3

    class Meta:
        model = Contacto
        exclude = ('escenario',)
