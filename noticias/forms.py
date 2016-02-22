from django import forms
from .models import Noticia
from coldeportes.utilities import MyDateWidget


class NoticiaForm(forms.ModelForm):
    required_css_class = 'required'

    class Meta:
        model = Noticia
        fields = ('titulo', 'fecha_inicio', 'fecha_expiracion', 'autor', 'cuerpo_noticia', 'etiquetas')

        widgets = {
            'fecha_inicio': MyDateWidget(),
            'fecha_expiracion': MyDateWidget()
        }