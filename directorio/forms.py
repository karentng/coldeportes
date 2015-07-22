from django import forms
from django.forms import ModelForm
from snd.models import *
from entidades.models import *
from datetimewidget.widgets import TimeWidget, DateWidget

  

class DirectorioBusquedaForm(forms.Form):
    texto_a_buscar = forms.CharField(help_text="Búsqueda")
    ciudad = form.Char
    def __init__(self, *args, **kwargs):
        super(IdentificacionForm, self).__init__(*args, **kwargs)
        self.fields['ciudad'] = adicionarClase(self.fields['ciudad'], 'one')
        self.fields['estrato'] = adicionarClase(self.fields['estrato'], 'one')
        self.fields['descripcion'].widget.attrs['rows'] = 3

    class Meta:
        model = Escenario
        exclude = ('entidad',)