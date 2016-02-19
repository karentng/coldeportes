from django import forms
from .models import Noticia
from django.utils.translation import ugettext_lazy as _


class NoticiaForm(forms.ModelForm):
    required_css_class = 'required'

    class Meta:
        model = Noticia
        fields = ('titulo','fecha_expiracion','autor','cuerpo_noticia','etiquetas')
        labels = {
            'titulo': _('Título'),
            'fecha_expiracion': _('Fecha Expiración'),
        }