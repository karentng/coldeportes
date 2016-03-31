#-*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from solicitudes_escenarios.solicitud.models import SolicitudEscenario,Escenario,AdjuntoSolicitud,DiscucionSolicitud
from coldeportes.utilities import adicionarClase,verificar_tamano_archivo
from entidades.models import Entidad

class SolicitudEscenarioForm(ModelForm):
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        super(SolicitudEscenarioForm, self).__init__(*args, **kwargs)
        self.fields['escenarios'] = adicionarClase(self.fields['escenarios'], 'many')
        self.fields['prioridad'] = adicionarClase(self.fields['prioridad'], 'one')
        self.fields['para_quien'] = adicionarClase(self.fields['para_quien'], 'one')
        self.fields['estado_actual_escenario'] = adicionarClase(self.fields['estado_actual_escenario'], 'one')
        self.fields['vinculo_solicitante'] = adicionarClase(self.fields['vinculo_solicitante'], 'one')
        self.fields['tipo'] = adicionarClase(self.fields['tipo'], 'one')
        self.fields['descripcion'].widget.attrs['rows'] = 3
        self.fields['para_quien'].queryset = Entidad.objects.filter(tipo=5)

    class Meta:
        model = SolicitudEscenario
        exclude = ('fecha','estado',)

class AdjuntoSolicitudForm(ModelForm):
    required_css_class = 'required'

    class Meta:
        model = AdjuntoSolicitud
        exclude = ('solicitud','discucion',)

class DiscusionForm(ModelForm):
    required_css_class = 'required'

    ESTADOS = (
        (2,'APROBADA'),
        (1,'INCOMPLETA'),
        (3,'RECHAZADA'),
    )

    def __init__(self, *args, **kwargs):
        super(DiscusionForm, self).__init__(*args, **kwargs)
        self.fields['estado_actual'] = adicionarClase(self.fields['estado_actual'], 'one')
        self.fields['estado_actual'].choices = self.ESTADOS
        self.fields['descripcion'].widget.attrs['rows'] = 3
        self.fields['descripcion'].widget.attrs['style'] = 'resize:none;'

    class Meta:
        model = DiscucionSolicitud
        exclude = ('solicitud','estado_anterior','fecha','entidad','respuesta',)

class EditarForm(ModelForm):
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        super(EditarForm, self).__init__(*args, **kwargs)
        self.fields['descripcion'].widget.attrs['rows'] = 3
        self.fields['descripcion'].widget.attrs['style'] = 'resize:none;'

    class Meta:
        model = DiscucionSolicitud
        exclude = ('solicitud','estado_anterior','fecha','entidad','estado_actual','respuesta',)