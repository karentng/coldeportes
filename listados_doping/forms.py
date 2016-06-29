from django import forms
from .models import CasoDoping
from coldeportes.utilities import adicionarClase

class CasoDopingForm(forms.ModelForm):
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        super(CasoDopingForm, self).__init__(*args, **kwargs)
        self.fields['tipo_sancion'] = adicionarClase(self.fields['tipo_sancion'], 'one')

    class Meta:
        model = CasoDoping
        exclude = ('estado',)
