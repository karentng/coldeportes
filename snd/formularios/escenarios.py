#-*- coding: utf-8 -*-
from django import forms
import datetime
from django.forms import ModelForm
from snd.models import *
from entidades.models import CaracteristicaEscenario, Dias
from datetimewidget.widgets import TimeWidget, DateWidget
from coldeportes.utilities import adicionarClase, MyDateWidget, extraer_codigo_video
from django.core.exceptions import ValidationError

class IdentificacionForm(forms.ModelForm):
    required_css_class = 'required'

    descripcion = forms.CharField(widget=forms.Textarea, required=False, label="Descripción")
    def __init__(self, *args, **kwargs):
        super(IdentificacionForm, self).__init__(*args, **kwargs)
        self.fields['ciudad'] = adicionarClase(self.fields['ciudad'], 'one')
        self.fields['estado'] = adicionarClase(self.fields['estado'], 'one')
        self.fields['estrato'] = adicionarClase(self.fields['estrato'], 'one')
        self.fields['division_territorial'] = adicionarClase(self.fields['division_territorial'], 'one')
        self.fields['descripcion'].widget.attrs['rows'] = 3

    def clean_nombre(self):
        try:
            nombre = self.cleaned_data['nombre'].upper()
            escenario = Escenario.objects.get(nombre = nombre)
            raise ValidationError('El nombre del escenario que está creando ya se encuentra registrado.')
        except Escenario.DoesNotExist:
            return self.cleaned_data['nombre']

    class Meta:
        model = Escenario
        exclude = ('entidad', 'fecha_creacion')


class IdentificacionEditarForm(forms.ModelForm):
    required_css_class = 'required'

    descripcion = forms.CharField(widget=forms.Textarea, required=False, label="Descripción")
    def __init__(self, *args, **kwargs):
        super(IdentificacionEditarForm, self).__init__(*args, **kwargs)
        self.fields['ciudad'] = adicionarClase(self.fields['ciudad'], 'one')
        self.fields['estrato'] = adicionarClase(self.fields['estrato'], 'one')
        self.fields['division_territorial'] = adicionarClase(self.fields['division_territorial'], 'one')
        self.fields['descripcion'].widget.attrs['rows'] = 3

    def clean_nombre(self):
        try:
            nombre = self.cleaned_data['nombre'].upper()
            escenario = Escenario.objects.get(nombre = nombre)
            if not escenario.id == self.instance.id:
                raise ValidationError('El nombre del escenario que está creando ya se encuentra registrado.')
            else:
                return self.cleaned_data['nombre']
        except Escenario.DoesNotExist: 
            return self.cleaned_data['nombre']

    class Meta:
        model = Escenario
        exclude = ('entidad', 'estado', 'fecha_creacion')

class CaracterizacionForm(forms.ModelForm):
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        super(CaracterizacionForm, self).__init__(*args, **kwargs)
        self.fields['tipo_escenario'] = adicionarClase(self.fields['tipo_escenario'], 'one')
        self.fields['clase_acceso'] = adicionarClase(self.fields['clase_acceso'], 'one')
        self.fields['estado_fisico'] = adicionarClase(self.fields['estado_fisico'], 'one')
        self.fields['tipo_propietario'] = adicionarClase(self.fields['tipo_propietario'], 'one')
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
        exclude = ('escenario', 'fecha_creacion') 


        

class HorariosDisponibleForm(ModelForm):
    required_css_class = 'required'

    hora_inicio = forms.TimeField(widget=TimeWidget(options={'format':'hh:ii'}))
    hora_fin = forms.TimeField(widget=TimeWidget(options={'format':'hh:ii'}))

    def __init__(self, *args, **kwargs):
        super(HorariosDisponibleForm, self).__init__(*args, **kwargs)
        self.fields['dias'] = adicionarClase(self.fields['dias'], 'many')
        self.fields['descripcion'].widget.attrs['rows'] = 3
        
    class Meta:

        model = HorarioDisponibilidad
        exclude = ('escenario', 'fecha_creacion')
        

class DatoHistoricoForm(ModelForm):
    required_css_class = 'required'
    
    fecha_fin = forms.DateField(widget=MyDateWidget(), required=False, label="Fecha fin del suceso histórico")
    def __init__(self, *args, **kwargs):
        super(DatoHistoricoForm, self).__init__(*args, **kwargs)
        self.fields['descripcion'].widget.attrs['rows'] = 3

    class Meta:
        model = DatoHistorico
        exclude = ('escenario', 'fecha_creacion')
        widgets = {
            'fecha_inicio': MyDateWidget(),
            'fecha_fin': MyDateWidget(),
        }
        
    def clean(self):
        cleaned_data = super(DatoHistoricoForm, self).clean()

        if not self._errors:
            try:
                fecha_inicio = cleaned_data.get('fecha_inicio')
            except Exception:
                fecha_inicio = None

            try:
                fecha_fin = cleaned_data.get('fecha_fin')
            except Exception:
                fecha_fin = None

           
            #Fecha de inicio no sea mayor a la fecha actual
            if fecha_inicio>datetime.date.today():                
                msg = 'Usted ha seleccionado una fecha de inicio mayor que la fecha actual'
                self.add_error('fecha_inicio',msg)                
            
            #Fecha de inicio no sea mayor que fecha fin
            if fecha_fin:
                if fecha_fin<fecha_inicio:
                    
                    msg = 'Usted ha seleccionado una fecha de menor que la fecha de inicio'
                    self.add_error('fecha_fin',msg)
                
            
        return cleaned_data
        

class FotoEscenarioForm(ModelForm):
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        super(FotoEscenarioForm, self).__init__(*args, **kwargs)
        self.fields['descripcion_foto'].widget.attrs['rows'] = 3

    class Meta:
        model = Foto
        exclude = ('escenario','fecha_creacion')

class MantenimientoEscenarioForm(ModelForm):
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        super(MantenimientoEscenarioForm, self).__init__(*args, **kwargs)
        self.fields['descripcion_ultimo_mantenimiento'].widget.attrs['rows'] = 3
        self.fields['razones_no_mantenimiento'].widget.attrs['rows'] = 3
        self.fields['periodicidad'] = adicionarClase(self.fields['periodicidad'], 'one')

    class Meta:
        model = Mantenimiento
        exclude = ('escenario', 'fecha_creacion')
        widgets = {
            'fecha_ultimo_mantenimiento': MyDateWidget(),
        }

    def clean(self):
        cleaned_data = super(MantenimientoEscenarioForm, self).clean()
        if not self._errors:
            try:
                fecha_mantenimiento = cleaned_data.get('fecha_ultimo_mantenimiento')
            except Exception:
                fecha_mantenimiento = None

            fecha_actual = datetime.date.today()
            if fecha_mantenimiento:
                if fecha_mantenimiento >= fecha_actual:
                    mensaje = 'La fecha no es válida, debe ser igual o anterior a la fecha actual'
                    self.add_error('fecha_ultimo_mantenimiento', mensaje)
                else:
                    return cleaned_data
            else:
                return cleaned_data

        return cleaned_data

class VideoEscenarioForm(ModelForm):
    required_css_class = 'required'

    def clean(self):
        cleaned_data = super(VideoEscenarioForm, self).clean()
        video = self.cleaned_data['url']
        if video:
            try:
                extraer_codigo_video(video)
            except Exception:
                self.add_error('url','Digite una url valida de un video de YouTube')
        return self.cleaned_data

    class Meta:
        model = Video
        exclude = ('escenario', 'fecha_creacion')

class ContactoForm(ModelForm):
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        super(ContactoForm, self).__init__(*args, **kwargs)
        self.fields['descripcion'].widget.attrs['rows'] = 3

    class Meta:
        model = Contacto
        exclude = ('escenario', 'fecha_creacion')
