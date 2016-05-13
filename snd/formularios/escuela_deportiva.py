# -*- coding: utf-8 -*-
from django import forms
from snd.models import (EscuelaDeportiva, Participante, Acudiente, CategoriaEscuela, HorarioActividadesEscuela,
                        AlertaTemprana, SeguimientoTallaPeso)
from datetimewidget.widgets import TimeWidget
from coldeportes.utilities import adicionarClase, verificar_tamano_archivo, MyDateWidget


class ParticipanteForm(forms.ModelForm):
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        sede_id = kwargs.pop('sede_id', None)
        super(ParticipanteForm, self).__init__(*args, **kwargs)
        self.fields['ciudad_residencia'] = adicionarClase(self.fields['ciudad_residencia'], 'one')
        self.fields['anho_curso'] = adicionarClase(self.fields['anho_curso'], 'one')
        self.fields['eps'] = adicionarClase(self.fields['eps'], 'one')
        self.fields['eps'].widget.attrs.update({'style': 'height: 71px;'})
        self.fields['nacionalidad'] = adicionarClase(self.fields['nacionalidad'], 'many')
        self.fields['sede_perteneciente'] = adicionarClase(self.fields['sede_perteneciente'], 'one')
        self.fields['etnia'] = adicionarClase(self.fields['etnia'], 'one')
        self.fields['categoria'].queryset = CategoriaEscuela.objects.none()
        if sede_id:
            self.fields['categoria'].queryset = CategoriaEscuela.objects.filter(sede=sede_id)

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
        self.fields['descripcion_lugar'].widget.attrs['rows'] = 3

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


class HorarioActividadesEscuelaForm(forms.ModelForm):

    required_css_class = 'required'
    hora_inicio = forms.TimeField(widget=TimeWidget(options={'format': 'hh:ii', 'language': 'es'}))
    hora_fin = forms.TimeField(widget=TimeWidget(options={'format': 'hh:ii', 'language': 'es'}))

    def __init__(self, *args, **kwargs):

        super(HorarioActividadesEscuelaForm, self).__init__(*args, **kwargs)
        self.fields['dias'] = adicionarClase(self.fields['dias'], 'many')
        self.fields['descripcion'].widget.attrs['rows'] = 4

    class Meta:
        model = HorarioActividadesEscuela
        exclude = ('sede', 'fecha_creacion',)


class CategoriaEscuelaForm(forms.ModelForm):
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):

        super(CategoriaEscuelaForm, self).__init__(*args, **kwargs)
        self.fields['descripcion'].widget.attrs['rows'] = 4

    class Meta:
        model = CategoriaEscuela
        exclude = ('sede', 'estado',)


class AlertaTempranaForm(forms.ModelForm):
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        super(AlertaTempranaForm, self).__init__(*args, **kwargs)
        self.fields['nivel_alerta'] = adicionarClase(self.fields['nivel_alerta'], 'one')
        self.fields['referencia_alerta'].widget.attrs['placeholder'] = 'Referecia (ej: desnutrición, drogadicción, etc)'
        self.fields['descripcion'].widget.attrs['rows'] = 4

    class Meta:
        model = AlertaTemprana
        exclude = ('participante', 'fecha_registro', 'fecha_ultima_actualizacion', 'estado', )


class SeguimientoTallaPesoForm(forms.ModelForm):
    required_css_class = 'required'

    class Meta:
        model = SeguimientoTallaPeso
        exclude = ('participante', 'fecha_registro', )
