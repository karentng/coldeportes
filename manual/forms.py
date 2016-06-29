#-*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from normograma.models import *
from coldeportes.utilities import adicionarClase
from django.forms.extras.widgets import SelectDateWidget
from manual.models import Articulo


class ArticuloForm(forms.ModelForm):
    required_css_class = 'required'

    class Meta:
        model = Articulo
        fields = '__all__'
        #exclude = ['contenido']
