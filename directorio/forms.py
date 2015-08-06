from django import forms
from django.forms import ModelForm
from snd.models import *
from entidades.models import *
from datetimewidget.widgets import TimeWidget, DateWidget
from coldeportes.utilities import adicionarClase
  
ACTORES = (
    ('CF', 'Cajas de Compensación'),
    ('CA', 'Centros de Acondicionamiento'),
    ('DE', 'Deportistas'),
    ('DI', 'Dirigentes'),
    ('EN', 'Entrenadores'),
    ('ES', 'Escenarios Deportivos'),
)

class DirectorioBusquedaForm(forms.Form):

    texto_a_buscar = forms.CharField(required=False, label="Búsqueda", widget=forms.TextInput(attrs={'placeholder': 'Ingrese las palabras clave'}))
    ciudad = forms.ModelMultipleChoiceField(queryset=Ciudad.objects.none(), required=False, widget=forms.SelectMultiple(attrs={'placeholder': 'Ciudad'}))
    actor = forms.MultipleChoiceField(label="Categoría", required=False, widget=forms.SelectMultiple(attrs={'placeholder': 'Categoría'}), choices=ACTORES)

    def __init__(self, *args, **kwargs):
        super(DirectorioBusquedaForm, self).__init__(*args, **kwargs)
        self.fields['ciudad'].queryset = Ciudad.objects.all()
        self.fields['ciudad'] = adicionarClase(self.fields['ciudad'], 'many')
        self.fields['actor'] = adicionarClase(self.fields['actor'], 'many')
