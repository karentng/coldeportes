from django import forms
from django.forms import ModelForm
from snd.models import Entrenador, FormacionDeportiva, ExperienciaLaboral
from coldeportes.utilities import adicionarClase


class EntrenadorForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(EntrenadorForm, self).__init__(*args, **kwargs)
        self.fields['ciudad'] = adicionarClase(self.fields['ciudad'], 'one')
        self.fields['nacionalidad'] = adicionarClase(self.fields['nacionalidad'], 'many')
        self.fields['fecha_nacimiento'] = adicionarClase(self.fields['fecha_nacimiento'], 'fecha')

    class Meta:
        model = Entrenador
        exclude = ('estado','entidad_vinculacion',)


class FormacionDeportivaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormacionDeportivaForm, self).__init__(*args, **kwargs)
        self.fields['disciplina_deportiva'] = adicionarClase(self.fields['disciplina_deportiva'], 'many')
        self.fields['pais_formacion'] = adicionarClase(self.fields['pais_formacion'], 'one')
        self.fields['fecha_comienzo'] = adicionarClase(self.fields['fecha_comienzo'], 'fecha')
        self.fields['fecha_fin'] = adicionarClase(self.fields['fecha_fin'], 'fecha')

    def clean(self):
        fecha_comienzo = self.cleaned_data['fecha_comienzo']
        fecha_fin = self.cleaned_data['fecha_fin']
        if fecha_fin != None:
            if fecha_fin < fecha_comienzo:
                msg = "La fecha de finalización es menor a la fecha de comienzo"
                self.add_error('fecha_comienzo', msg)
                self.add_error('fecha_fin', msg)

    class Meta:
        model = FormacionDeportiva
        exclude = ('entrenador',)


class ExperienciaLaboralForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ExperienciaLaboralForm, self).__init__(*args, **kwargs)
        self.fields['fecha_comienzo'] = adicionarClase(self.fields['fecha_comienzo'], 'fecha')
        self.fields['fecha_fin'] = adicionarClase(self.fields['fecha_fin'], 'fecha')

    def clean(self):
        fecha_comienzo = self.cleaned_data['fecha_comienzo']
        fecha_fin = self.cleaned_data['fecha_fin']
        if fecha_fin != None:
            if fecha_fin < fecha_comienzo:
                msg = "La fecha de finalización es menor a la fecha de comienzo"
                self.add_error('fecha_comienzo', msg)
                self.add_error('fecha_fin', msg)

    class Meta:
        model = ExperienciaLaboral
        exclude = ('entrenador',)
