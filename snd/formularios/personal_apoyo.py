from django import forms
from django.forms import ModelForm
from snd.models import PersonalApoyo, FormacionDeportiva, ExperienciaLaboral
from coldeportes.utilities import adicionarClase,MyDateWidget


class PersonalApoyoForm(ModelForm):
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        super(PersonalApoyoForm, self).__init__(*args, **kwargs)
        self.fields['ciudad'] = adicionarClase(self.fields['ciudad'], 'one')
        self.fields['tipo_id'] = adicionarClase(self.fields['tipo_id'], 'one')
        self.fields['genero'] = adicionarClase(self.fields['genero'], 'one')
        self.fields['etnia'] = adicionarClase(self.fields['etnia'], 'one')
        self.fields['actividad'] = adicionarClase(self.fields['actividad'], 'one')
        self.fields['nacionalidad'] = adicionarClase(self.fields['nacionalidad'], 'many')

    class Meta:
        model = PersonalApoyo
        exclude = ('estado','entidad',)
        widgets = {
            'fecha_nacimiento': MyDateWidget(),
        }


class VerificarExistenciaForm(forms.Form):
    TIPO_IDENTIDAD = (
        ('CC', 'CÉDULA DE CIUDADANÍA'),
        ('CE', 'CÉDULA DE EXTRANJERÍA'),
        ('PS', 'PASAPORTE'),
    )
    tipo_id = forms.ChoiceField(label='Tipo de documento',choices=TIPO_IDENTIDAD)
    identificacion = forms.CharField(label="Identificación del personal de apoyo")



class FormacionDeportivaForm(ModelForm):

    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        super(FormacionDeportivaForm, self).__init__(*args, **kwargs)
        self.fields['nivel'] = adicionarClase(self.fields['nivel'], 'one')
        self.fields['estado'] = adicionarClase(self.fields['estado'], 'one')
        self.fields['pais'] = adicionarClase(self.fields['pais'], 'one')

    class Meta:
        model = FormacionDeportiva
        exclude = ('personal_apoyo',)

class ExperienciaLaboralForm(ModelForm):
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        super(ExperienciaLaboralForm, self).__init__(*args, **kwargs)

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
        widgets = {
            'fecha_comienzo': MyDateWidget(),
            'fecha_fin': MyDateWidget(),
        }
