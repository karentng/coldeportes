#-*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from coldeportes.utilities import adicionarClase, verificar_tamano_archivo
from entidades.models import Entidad
from reconocimiento_deportivo.modelos.solicitudes import ReconocimientoDeportivo, AdjuntoReconocimiento, DiscusionReconocimiento

class ReconocimientoDeportivoForm(ModelForm):
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        super(ReconocimientoDeportivoForm, self).__init__(*args, **kwargs)
        self.fields['para_quien'] = adicionarClase(self.fields['para_quien'], 'one')
        self.fields['vinculo_solicitante'] = adicionarClase(self.fields['vinculo_solicitante'], 'one')
        self.fields['tipo'] = adicionarClase(self.fields['tipo'], 'one')
        self.fields['descripcion'].widget.attrs['rows'] = 3
        self.fields['para_quien'].queryset = Entidad.objects.filter(tipo=5)

    class Meta:
        model = ReconocimientoDeportivo
        fields = ('descripcion', 'para_quien', 'nombre_solicitante', 'tipo', 'id_solicitante', 'tel_solicitante', 'direccion_solicitante', 'vinculo_solicitante')

    def clean_club(self):

        marca = self.cleaned_data['marca']
        if marca:
            try:
                if marca.isdigit() or "." in marca or ":" in marca:
                    return self.cleaned_data['marca']
                else:
                    raise ValidationError('La marca debe tener números, puntos y/o dos puntos. Ej: 24.100, 03:05')
            except:
                raise ValidationError('La marca debe tener números, puntos y/o dos puntos. Ej: 24.100, 03:05')
        else:
            pass


class AdjuntoReconocimientoForm(ModelForm):

    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        super(AdjuntoReconocimientoForm, self).__init__(*args, **kwargs)
        self.fields['tipo'] = adicionarClase(self.fields['tipo'], 'one')

    class Meta:
        model = AdjuntoReconocimiento
        exclude = ('solicitud', 'discusion')


class DiscusionForm(ModelForm):
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        super(DiscusionForm, self).__init__(*args, **kwargs)
        self.fields['descripcion'].widget.attrs['rows'] = 3
        self.fields['descripcion'].widget.attrs['style'] = 'resize:none;'

    class Meta:
        model = DiscusionReconocimiento
        exclude = ('solicitud','estado_anterior','fecha','entidad','estado_actual','respuesta',)
