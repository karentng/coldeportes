from django import forms
from .models import Noticia
from coldeportes.utilities import verificar_tamano_archivo


class NoticiaForm(forms.ModelForm):
    required_css_class = 'required'

    def clean(self):
        cleaned_data = super(NoticiaForm, self).clean()
        self = verificar_tamano_archivo(self, cleaned_data, "foto")
        return self.cleaned_data

    class Meta:
        model = Noticia
        fields = '__all__'