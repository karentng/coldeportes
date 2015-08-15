from django import forms
from django.forms import ModelForm
from snd.models import PersonalApoyo, FormacionDeportiva, ExperienciaLaboral
from coldeportes.utilities import adicionarClase


class PersonalApoyoForm(ModelForm):
    fecha_nacimiento = forms.DateField(widget=forms.DateInput(format = '%Y-%m-%d'), input_formats=('%Y-%m-%d',))
    def __init__(self, *args, **kwargs):
        super(PersonalApoyoForm, self).__init__(*args, **kwargs)
        self.fields['ciudad'] = adicionarClase(self.fields['ciudad'], 'one')
        self.fields['tipo_id'] = adicionarClase(self.fields['tipo_id'], 'one')
        self.fields['genero'] = adicionarClase(self.fields['genero'], 'one')
        self.fields['etnia'] = adicionarClase(self.fields['etnia'], 'one')
        self.fields['actividad'] = adicionarClase(self.fields['actividad'], 'one')
        self.fields['nacionalidad'] = adicionarClase(self.fields['nacionalidad'], 'many')
        self.fields['fecha_nacimiento'] = adicionarClase(self.fields['fecha_nacimiento'], 'fecha')

    class Meta:
        model = PersonalApoyo
        exclude = ('estado','entidad',)


class VerificarExistenciaForm(forms.Form):
    """TIPO_IDENTIDAD = (
        ('CED', 'CÉDULA DE CIUDADANÍA'),
        ('CEDEX', 'CÉDULA DE EXTRANJERO'),
        ('PAS', 'PASAPORTE'),
    )
    tipo_id = forms.ChoiceField(choices=TIPO_IDENTIDAD)"""
    identificacion = forms.IntegerField(label="Identificación del personal de apoyo")



class FormacionDeportivaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormacionDeportivaForm, self).__init__(*args, **kwargs)
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
        exclude = ('personal_apoyo',)


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
        exclude = ('personal_apoyo',)
