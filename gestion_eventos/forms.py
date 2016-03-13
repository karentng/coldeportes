from django import forms
from .models import *
from coldeportes.utilities import MyDateWidget, MyDateTimeWidget
from datetimewidget.widgets import TimeWidget


class EventoForm(forms.ModelForm):
    required_css_class = 'required'

    class Meta:
        model = Evento
        fields = ('titulo_evento','lugar_evento', 'fecha_inicio', 'fecha_finalizacion', 'fecha_inicio_preinscripcion',
                  'fecha_finalizacion_preinscripcion', 'fecha_inicio_inscripcion', 'fecha_finalizacion_inscripcion',
                  'descripcion_evento', 'video', 'cupo_participantes', 'costo_entrada', 'autor')

        widgets = {
            'fecha_inicio': MyDateWidget(),
            'fecha_finalizacion': MyDateWidget(),
            'fecha_inicio_preinscripcion': MyDateWidget(),
            'fecha_finalizacion_preinscripcion': MyDateWidget(),
            'fecha_inicio_inscripcion': MyDateWidget(),
            'fecha_finalizacion_inscripcion': MyDateWidget()
        }

class ParticipanteForm(forms.ModelForm):
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        super(ParticipanteForm, self).__init__(*args, **kwargs)
        self.fields['tipo_id'].widget.attrs.update({'readonly': True, 'style':'pointer-events:none;'})
        self.fields['identificacion'].widget.attrs.update({'readonly': True})

    class Meta:
        model = Participante
        fields = ('nombre','apellido', 'tipo_id', 'identificacion', 'fecha_nacimiento',
                  'email')

        widgets = {
            'fecha_nacimiento': MyDateWidget()
        }


class ActividadForm(forms.ModelForm):
    required_css_class = 'required'

    hora_inicio = forms.TimeField(widget=TimeWidget(options={'format':'hh:ii'}))
    hora_fin = forms.TimeField(widget=TimeWidget(options={'format':'hh:ii'}))

    class Meta:
        model = Actividad
        fields = ('titulo','descripcion', 'dia_actividad', 'hora_inicio', 'hora_fin')

        widgets = {
            'dia_actividad': MyDateWidget(),
            'hora_inicio': MyDateTimeWidget()
        }