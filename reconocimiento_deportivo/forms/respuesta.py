from django import forms
from django.forms import ModelForm
from coldeportes.utilities import adicionarClase, verificar_tamano_archivo
from reconocimiento_deportivo.modelos.solicitudes import DiscusionReconocimiento


class ResponderSolicitudForm(ModelForm):

    required_css_class = 'required'

    ESTADOS = (
        (2,'APROBADA'),
        (1,'INCOMPLETA'),
        (3,'RECHAZADA'),
    )

    def __init__(self, *args, **kwargs):
        super(ResponderSolicitudForm, self).__init__(*args, **kwargs)
        self.fields['estado_actual'] = adicionarClase(self.fields['estado_actual'], 'one')
        self.fields['estado_actual'].choices = self.ESTADOS
        self.fields['descripcion'].widget.attrs['rows'] = 3
        self.fields['descripcion'].widget.attrs['style'] = 'resize:none;'

    class Meta:
        model = DiscusionReconocimiento
        exclude = ('solicitud', 'estado_anterior', 'fecha', 'entidad', 'respuesta',)