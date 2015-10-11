from django import forms
from django.forms import ModelForm
from snd.models import *
from coldeportes.utilities import adicionarClase
import datetime
from coldeportes.utilities import MyDateWidget


class DirigenteVerificarExistenciaForm(forms.Form):
    TIPO_IDENTIDAD = (
        ('CC', 'CÉDULA DE CIUDADANÍA'),
        ('CE', 'CÉDULA DE EXTRANJERÍA'),
        ('PS', 'PASAPORTE'),
    )
    tipo_identificacion = forms.ChoiceField(label='Tipo de documento',choices=TIPO_IDENTIDAD)
    identificacion = forms.CharField(label="Identificación del dirigente")

class DirigenteForm(ModelForm):

    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        super(DirigenteForm, self).__init__(*args, **kwargs)
        self.fields['nacionalidad'] = adicionarClase(self.fields['nacionalidad'], 'many')
        self.fields['ciudad_residencia'] = adicionarClase(self.fields['ciudad_residencia'], 'one')
        self.fields['tipo_identificacion'] = adicionarClase(self.fields['tipo_identificacion'], 'one')
        self.fields['genero'] = adicionarClase(self.fields['genero'], 'one')
        self.fields['perfil'].widget.attrs['rows'] = 3


    class Meta:
        model = Dirigente
        #fields = '__all__'
        exclude = ('entidad', 'estado',)

class DirigenteCargosForm(ModelForm):
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        dirigente_id = kwargs.pop('dirigente_id', False)
        super(DirigenteCargosForm, self).__init__(*args, **kwargs)
        self.fields['superior'] = adicionarClase(self.fields['superior'], 'one')
        self.fields['superior_cargo'] = adicionarClase(self.fields['superior_cargo'], 'one')
        if dirigente_id:
            self.fields['superior'].queryset = Dirigente.objects.exclude(id=dirigente_id)

    def clean(self):
        cleaned_data = super(DirigenteCargosForm, self).clean()
        if not self._errors:
            msg = []
            fecha_posesion = cleaned_data.get("fecha_posesion")
            fecha_retiro = cleaned_data.get("fecha_retiro")
            vigencia_inicio = cleaned_data.get("vigencia_inicio")
            vigencia_fin = cleaned_data.get("vigencia_fin")

            if vigencia_fin < vigencia_inicio:
                msg.append(("vigencia_inicio","La fecha de fin de vigencia del periodo debe de ser mayor que su fecha de inicio"))
            if vigencia_inicio > datetime.date.today():
                msg.append(("vigencia_inicio","La fecha de inicio de vigencia del periodo no puede ser mayor el día de hoy"))
            if fecha_retiro != None:
                if fecha_retiro < fecha_posesion:
                    msg.append(("fecha_retiro","La fecha de retiro debe de ser mayor que la fecha de posesión"))
                if fecha_retiro > datetime.date.today():
                    msg.append(("fecha_retiro","La fecha de retiro no puede ser mayor que el día de hoy"))
                if fecha_retiro < vigencia_inicio or fecha_retiro > vigencia_fin:
                    msg.append(("fecha_retiro","La fecha de retiro debe de encontrarse dentro del periodo de vigencia"))
            if fecha_posesion > datetime.date.today():
                msg.append(("fecha_posesion","La fecha de posesión no puede ser mayor que el día de hoy"))
            if fecha_posesion < vigencia_inicio or fecha_posesion > vigencia_fin:
                msg.append(("fecha_posesion","La fecha de posesión debe de encontrarse dentro del periodo de vigencia"))

            for campo,mensaje in msg:
                self.add_error(campo,mensaje)

        return cleaned_data

    class Meta:
        model = DirigenteCargo
        exclude = ('dirigente',)
        widgets = {
            'fecha_posesion':MyDateWidget(),
            'fecha_retiro':MyDateWidget(),
            'vigencia_inicio':MyDateWidget(),
            'vigencia_fin':MyDateWidget(),
        }

class DirigenteFuncionesForm(ModelForm):

    required_css_class = 'required'
    dirigente = forms.CharField()

    def __init__(self, *args, **kwargs):
        dirigente_id = kwargs.pop('dirigente_id', False)
        cargo_id = kwargs.pop('cargo_id', False)
        super(DirigenteFuncionesForm, self).__init__(*args, **kwargs)
        if dirigente_id:
            self.fields['cargo'].queryset=DirigenteCargo.objects.filter(dirigente=dirigente_id)
            self.fields['dirigente'].widget = forms.HiddenInput()
            self.fields['dirigente'].initial = dirigente_id
            self.fields['cargo'] = adicionarClase(self.fields['cargo'], 'one')
        if cargo_id:
            self.fields['cargo'].initial = cargo_id

    class Meta:
        model = DirigenteFuncion
        exclude = ('dirigente',)