from django import forms
from .models import CasoDoping


class CasoDopingForm(forms.ModelForm):
    required_css_class = 'required'

    class Meta:
        model = CasoDoping
        exclude = ('estado',)
