from django import forms
from django.forms import ModelForm
from normograma.models import *
from coldeportes.utilities import adicionarClase
from django.forms.extras.widgets import SelectDateWidget


class NormaForm(forms.ModelForm):
    sectores = (
        ('D', 'Deporte'),
        ('E', 'Educación Física'),
        ('R', 'Recreación'),
    )
    sector = forms.MultipleChoiceField(label="Sector", widget=forms.SelectMultiple(attrs={'placeholder': 'Sector'}), choices=sectores)

    def __init__(self, *args, **kwargs):
        super(NormaForm, self).__init__(*args, **kwargs)
        self.fields['sector'] = adicionarClase(self.fields['sector'], 'many')
        self.fields['año'] = adicionarClase(self.fields['año'], 'one')
        self.fields['descripcion'].widget.attrs['rows'] = 3
        self.fields['palabras_clave'].widget.attrs['rows'] = 3
    class Meta:
        model = Norma
        fields = '__all__'