# -*- encoding: utf-8 -*-
from django import forms
from registro_resultados.models import *
from coldeportes.utilities import adicionarClase, MyDateWidget

class JuegoForm(forms.ModelForm):
    required_css_class = 'required'
    
    def __init__(self, *args, **kwargs):
        super(JuegoForm, self).__init__(*args, **kwargs)
        self.fields['pais'] = adicionarClase(self.fields['pais'], 'one')
        self.fields['descripcion'].widget.attrs['rows'] = 3


    class Meta:
        model = Juego
        exclude = ()

class CompetenciaForm(forms.ModelForm):
    required_css_class = 'required'

    TIPOS_REGISTROS = (
        (1, "Tiempos"),
        (2, "Puntos"),
    )
    tipo_registro = forms.ChoiceField(widget=forms.RadioSelect, choices=TIPOS_REGISTROS, label='Registros De Competencia')

    def __init__(self, *args, **kwargs):
        deporte_id = kwargs.pop('deporte_id',None)
        super(CompetenciaForm, self).__init__(*args, **kwargs)
        self.fields['deporte'] = adicionarClase(self.fields['deporte'], 'one')
        self.fields['deporte'].queryset = TipoDisciplinaDeportiva.objects.all().order_by('descripcion')
        self.fields['descripcion'].widget.attrs['rows'] = 3

        if deporte_id:
            self.fields['categoria'].queryset = CategoriaDisciplinaDeportiva.objects.filter(deporte=deporte_id).order_by('nombre')
            self.fields['modalidad'].queryset = ModalidadDisciplinaDeportiva.objects.filter(deporte=deporte_id).order_by('nombre')

    class Meta:
        model = Competencia
        exclude = ('juego',)
        widgets = {
            'fecha_competencia': MyDateWidget(),
        }

class ParticipanteForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        competencia = kwargs.pop('competencia')
        super(ParticipanteForm, self).__init__(*args, **kwargs)
        self.fields['departamento'] = adicionarClase(self.fields['departamento'], 'one')
        if competencia.tiempos != True:
            del self.fields['tiempo']

        if competencia.tipos_participantes == 1:
            del self.fields['equipo']

    class Meta:
        model = Participante
        exclude = ("competencia",)

class EquipoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EquipoForm, self).__init__(*args, **kwargs)
        self.fields['departamento'] = adicionarClase(self.fields['departamento'], 'one')

    class Meta:
        model = Equipo
        exclude = ("competencia",)