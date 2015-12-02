from django import forms
from entidades.models import Departamento,TipoDisciplinaDeportiva
from coldeportes.utilities import adicionarClase

VISUALIZACIONES = (
    (1, "Dona"),
    (2, "Gráfica de líneas"),
    (3, "Gráfica de barras"),
    (4, "Tree Map"), 
    (5, "Gráfica de cilindros"),
    (6, "Gráfica de cono"),
    (7, "Gráfica de radar"),
)

class DemografiaForm(forms.Form):
    def __init__(self, *args, **kwargs):
        visualizaciones_definidas = kwargs.pop('visualizaciones', None)
        super(DemografiaForm, self).__init__(*args, **kwargs)
        self.fields['departamento'] = adicionarClase(self.fields['departamento'], 'many')
        self.fields['visualizacion'] = adicionarClase(self.fields['visualizacion'], 'one')
        self.fields['anno'] = adicionarClase(self.fields['anno'], 'many')

        visualizaciones = tuple()
        if visualizaciones_definidas:
            for i in self.fields['visualizacion'].choices:
                if i[0] in visualizaciones_definidas:
                    visualizaciones += (i,)
            self.fields['visualizacion'].choices = visualizaciones

    departamento = forms.ModelMultipleChoiceField(queryset=Departamento.objects.all(), required=False)
    anno = forms.MultipleChoiceField(choices=((2013, 2013),(2014, 2014),(2015, 2015),),required=False, label="Año")
    visualizacion = forms.ChoiceField(choices=VISUALIZACIONES)