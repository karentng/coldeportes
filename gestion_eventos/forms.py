from django import forms
from .models import Evento
from coldeportes.utilities import MyDateWidget


class EventoForm(forms.ModelForm):
    required_css_class = 'required'

    class Meta:
        model = Evento
        fields = ('titulo_evento','lugar_evento', 'fecha_inicio', 'fecha_finalizacion', 'fecha_inicio_preinscripcion',
                  'fecha_finalizacion_preinscripcion', 'video', 'descripcion_evento', 'costo_entrada',
                  'cupo_participantes', 'autor')

        widgets = {
            'fecha_inicio': MyDateWidget(),
            'fecha_finalizacion': MyDateWidget(),
            'fecha_inicio_preinscripcion': MyDateWidget(),
            'fecha_finalizacion_preinscripcion': MyDateWidget()
        }