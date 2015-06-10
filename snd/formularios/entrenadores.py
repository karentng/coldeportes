from django import forms
from django.forms import ModelForm
from snd.models import Entrenador, FormacionDeportiva, ExperienciaLaboral
from datetimewidget.widgets import DateWidget

def adicionarClase(campo, clase):
    campo.widget.attrs.update({'class': clase})
    return campo


class EntrenadorForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(EntrenadorForm, self).__init__(*args, **kwargs)
        self.fields['ciudad'] = adicionarClase(self.fields['ciudad'], 'one')
        self.fields['nacionalidad'] = adicionarClase(self.fields['nacionalidad'], 'one')
        self.fields['tipo_id'] = adicionarClase(self.fields['tipo_id'], 'one')
    class Meta:
        model = Entrenador
        exclude = ('estado','entidad_vinculacion',)
        widgets = {
            'fecha_nacimiento': DateWidget(attrs={'id':"id_fecha_nacimiento"}, options={'format': 'yyyy-mm-dd'}, usel10n = True, bootstrap_version=3)
        }

class FormacionDeportivaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormacionDeportivaForm, self).__init__(*args, **kwargs)
        self.fields['disciplina_deportiva'] = adicionarClase(self.fields['disciplina_deportiva'], 'one')
        self.fields['pais_formacion'] = adicionarClase(self.fields['pais_formacion'], 'one')

    class Meta:
        model = FormacionDeportiva
        exclude = ('entrenador',)
        widgets = {
            'fecha_comienzo': DateWidget(attrs={'id':"id_fecha_comienzo"}, options={'format': 'yyyy-mm-dd'}, usel10n = True, bootstrap_version=3),
            'fecha_fin': DateWidget(attrs={'id':"id_fecha_fin"}, options={'format': 'yyyy-mm-dd'}, usel10n = True, bootstrap_version=3)
        }

class ExperienciaLaboralForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ExperienciaLaboralForm, self).__init__(*args, **kwargs)
    class Meta:
        model = ExperienciaLaboral
        exclude = ('entrenador',)
        widgets = {
            'fecha_comienzo': DateWidget(attrs={'id':"id_fecha_comienzo"}, options={'format': 'yyyy-mm-dd'}, usel10n = True, bootstrap_version=3),
            'fecha_fin': DateWidget(attrs={'id':"id_fecha_fin"}, options={'format': 'yyyy-mm-dd'}, usel10n = True, bootstrap_version=3)
        }