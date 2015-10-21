from django import forms
from .models import Noticia


class NoticiaForm(forms.ModelForm):
    required_css_class = 'required'
    class Meta:
        model = Noticia
        fields = '__all__'