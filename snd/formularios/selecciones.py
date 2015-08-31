#-*- coding: utf-8 -*-
from django import forms
from django.contrib.contenttypes.models import ContentType
from django.db import connection
from django.forms import ModelForm
from snd.models import *
import datetime
from coldeportes.utilities import adicionarClase


class SeleccionForm(ModelForm):
    required_css_class = 'required'

    def __init__(self,*args, **kwargs):
        super(SeleccionForm, self).__init__(*args, **kwargs)
        self.fields['tipo'].widget.attrs.update({'readonly': True})
        self.fields['tipo_campeonato'] = adicionarClase(self.fields['tipo_campeonato'], 'one')
        self.fields['fecha_inicial'] = adicionarClase(self.fields['fecha_inicial'],'fecha')
        self.fields['fecha_final'] = adicionarClase(self.fields['fecha_final'],'fecha')

    class Meta:
        model = Seleccion
        exclude = ('deportistas','personal_apoyo',)

"""
class SeleccionDeportistasForm(forms.Form):

    deportistas = forms.ModelChoiceField(widget=forms.Select(attrs={'id':'sele-depor','class':'one'}),label='Seleccione un deportista',queryset=None)

    def __init__(self,tenant,*args, **kwargs):
        super(SeleccionDeportistasForm, self).__init__(*args, **kwargs)
        depor = self.get_deportistas(tenant)
        self.fields['deportistas'].queryset = depor

    def get_deportistas(self,tenant):
        if tenant.tipo == 1:
            #Liga
            clubes = Club.objects.filter(liga=tenant.id)
            connection.set_tenant(clubes[0])
            ContentType.objects.clear_cache()
            depor = Deportista.objects.all()
            return depor
        elif tenant.tipo == 2:
            #Fede
            pass
"""