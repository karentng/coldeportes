#-*- coding: utf-8 -*-
from django import forms
from django.contrib.contenttypes.models import ContentType
from django.db import connection
from django.forms import ModelForm
from snd.models import *
import datetime
from coldeportes.utilities import adicionarClase,MyDateWidget


class SeleccionForm(ModelForm):
    required_css_class = 'required'

    def __init__(self,*args, **kwargs):
        super(SeleccionForm, self).__init__(*args, **kwargs)
        self.fields['tipo'].widget.attrs.update({'readonly': True})
        self.fields['tipo_campeonato'] = adicionarClase(self.fields['tipo_campeonato'], 'one')

    class Meta:
        model = Seleccion
        exclude = ('deportistas','personal_apoyo','estado',)
        widgets = {
            'fecha_inicial': MyDateWidget(),
            'fecha_final': MyDateWidget(),
        }
