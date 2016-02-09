from coldeportes.utilities import adicionarClase
from entidades.models import Departamento
from reportes.forms import VISUALIZACIONES


class FiltrosPersonalApoyoForm(forms.Form):
    """
    Formulario para filtros de personal de apoyo
    """
    def __init__(self, *args, **kwargs):
        visualizaciones_definidas = kwargs.pop('visualizaciones', None)
        super(FiltrosPersonalApoyoForm, self).__init__(*args, **kwargs)
        self.fields['departamento'] = adicionarClase(self.fields['departamento'], 'many')
        self.fields['visualizacion'] = adicionarClase(self.fields['visualizacion'], 'one')
        self.fields['genero'] = adicionarClase(self.fields['genero'], 'many')

        visualizaciones = tuple()
        if visualizaciones_definidas:
            for i in self.fields['visualizacion'].choices:
                if i[0] in visualizaciones_definidas:
                    visualizaciones += (i,)
            self.fields['visualizacion'].choices = visualizaciones

    departamento = forms.ModelMultipleChoiceField(queryset=Departamento.objects.all(), required=False)
    genero = forms.MultipleChoiceField(choices=(('HOMBRE','MASCULINO'),('MUJER','FEMENINO'),),required=False, label="Género")
    visualizacion = forms.ChoiceField(choices=VISUALIZACIONES, label="Visualización")