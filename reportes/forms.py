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


