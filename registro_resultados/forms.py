# -*- encoding: utf-8 -*-
from django import forms
from registro_resultados.models import *
from coldeportes.utilities import adicionarClase, MyDateWidget

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
        self.fields['disciplina_deportiva'] = adicionarClase(self.fields['disciplina_deportiva'], 'one')
        self.fields['categoria'] = adicionarClase(self.fields['categoria'], 'one')
        self.fields['categoria'].queryset = CategoriaDisciplinaDeportiva.objects.none()
        self.fields['modalidad'].queryset = ModalidadDisciplinaDeportiva.objects.none()
        self.fields['disciplina_deportiva'].queryset = TipoDisciplinaDeportiva.objects.all().order_by('descripcion')
        if deporte_id:
            self.fields['categoria'].queryset = CategoriaDisciplinaDeportiva.objects.filter(deporte=deporte_id).order_by('nombre')
            self.fields['modalidad'].queryset = ModalidadDisciplinaDeportiva.objects.filter(deporte=deporte_id).order_by('nombre')

    class Meta:
        model = Competencia
        exclude = ()
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