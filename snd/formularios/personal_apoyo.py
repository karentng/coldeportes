import datetime
from django import forms
from entidades.models import TipoDisciplinaDeportiva
from django.forms import ModelForm
from snd.models import PersonalApoyo, FormacionDeportiva, ExperienciaLaboral
from coldeportes.utilities import adicionarClase,MyDateWidget, verificar_tamano_archivo


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

    def validar_id(self):
        tipo_id = self.data['tipo_id']
        identificacion = self.data['identificacion']
        if tipo_id == 'CC' and not identificacion.isdigit():
            msg = 'El tipo de identificación CÉDULA DE CIUDADANÍA solo puede contener números'
            self.add_error('identificacion',msg)
            self.add_error('tipo_id',msg)
        else:
            return True


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

    def clean(self):
        cleaned_data = super(FormacionDeportivaForm, self).clean()
        if not self._errors:
            estado = cleaned_data.get('estado')
            try:
                anio_finalizacion =cleaned_data.get('fecha_finalizacion')
            except Exception:
                anio_finalizacion = None

            anio_actual = datetime.datetime.now().year
            if anio_finalizacion:
                if estado == 'Finalizado' and int(anio_finalizacion) > anio_actual:
                    msg = 'Usted ha seleccionado el estado FINALIZADO con una fecha mayor a la actual'
                    self.add_error('fecha_finalizacion',msg)
                else:
                    return cleaned_data
            else:
                return cleaned_data
        return cleaned_data


class ExperienciaLaboralForm(ModelForm):
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        super(ExperienciaLaboralForm, self).__init__(*args, **kwargs)
        deporte_id = kwargs.pop('deporte_id', None)
        self.fields['deporte'] = adicionarClase(self.fields['deporte'], 'one')
        self.fields['modalidad'] = adicionarClase(self.fields['modalidad'], 'one')  
        self.fields['deporte'].queryset = TipoDisciplinaDeportiva.objects.all().order_by('descripcion')      
        if deporte_id:
            self.fields['modalidad'].queryset = ModalidadDisciplinaDeportiva.objects.filter(deporte = deporte_id).order_by('nombre')

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
