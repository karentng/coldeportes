from django import forms
from django.forms import ModelForm
from snd.models import *
from datetimewidget.widgets import DateWidget

def adicionarClase(campo, clase):
    campo.widget.attrs.update({'class': clase})
    return campo

class DirigenteForm(ModelForm):

    descripcion = forms.CharField(widget=forms.Textarea, required=True)

    def __init__(self, *args, **kwargs):
        super(DirigenteForm, self).__init__(*args, **kwargs)
        self.fields['superior'] = adicionarClase(self.fields['superior'], 'one')
        self.fields['nacionalidad'] = adicionarClase(self.fields['nacionalidad'], 'many')

    class Meta:
        model = Dirigente
        #fields = '__all__'
        exclude = ('entidad','activo',)
        widgets = {
            'fecha_posecion': DateWidget(attrs={'id':"id_fecha_posecion"}, options={'format': 'yyyy-mm-dd'}, usel10n = True, bootstrap_version=3),
            'fecha_retiro': DateWidget(attrs={'id':"id_fecha_retiro"}, options={'format': 'yyyy-mm-dd'}, usel10n = True, bootstrap_version=3)
        }

class DirigenteFuncionesForm(ModelForm):

    descripcion = forms.CharField(widget=forms.Textarea, required=True)
    
    class Meta:
        model = Funcion
        exclude = ('dirigente',)