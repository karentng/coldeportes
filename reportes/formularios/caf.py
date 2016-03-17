from django import forms
from entidades.models import Departamento,TipoDisciplinaDeportiva, Ciudad
from coldeportes.utilities import adicionarClase
from reportes.utilities import add_visualizacion

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

class FiltrosCafDMDForm(forms.Form):
    
    TIPO_REPORTE = (
        ('ES', 'Estratos Socioeconómicos'),
        ('DT', 'Centros de acondicionamiento por departamento'),
        ('CC', 'Clases ofrecidas por el CAF'),
        ('SC', 'Servicios ofrecidos por el CAF'),
    )
    def __init__(self, *args, **kwargs):
        visualizaciones_definidas = kwargs.pop('visualizaciones', None)
        eliminar = kwargs.pop('eliminar', None)
        super(FiltrosCafDMDForm, self).__init__(*args, **kwargs)
        self.fields['departamentos'] = adicionarClase(self.fields['departamentos'], 'many')
        self.fields['municipios'] = adicionarClase(self.fields['municipios'], 'many')
        self.fields['visualizacion'] = adicionarClase(self.fields['visualizacion'], 'one')
        self.fields['reporte'] = adicionarClase(self.fields['reporte'], 'one')

        if eliminar:
            del self.fields[eliminar]


        add_visualizacion(self.fields['visualizacion'], visualizaciones_definidas)

    departamentos = forms.ModelMultipleChoiceField(queryset=Departamento.objects.all(), required=False)
    municipios = forms.ModelMultipleChoiceField(queryset=Ciudad.objects.all(), required=False)
    reporte = forms.ChoiceField(label="Clasificar por:",required=False,choices=TIPO_REPORTE)
    visualizacion = forms.ChoiceField(label="Visualización")