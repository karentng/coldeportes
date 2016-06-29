#-*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from coldeportes.utilities import adicionarClase,MyDateTimeWidget
from entidades.models import Entidad,CalendarioNacional,TipoDisciplinaDeportiva,CategoriaDisciplinaDeportiva,ModalidadDisciplinaDeportiva

class CalendarioForm(ModelForm):
    required_css_class = 'required'
    def __init__(self, *args, **kwargs):
        deporte_id = kwargs.pop('deporte_id',None)
        super(CalendarioForm, self).__init__(*args, **kwargs)
        self.fields['tipo'] = adicionarClase(self.fields['tipo'], 'one')
        #self.fields['tipo'].widget.attrs.update({'readonly': True}) #Mientras se definen los otros tipos
        self.fields['ciudad'] = adicionarClase(self.fields['ciudad'], 'one')
        self.fields['modalidad'] = adicionarClase(self.fields['modalidad'], 'one')
        self.fields['categoria'] = adicionarClase(self.fields['categoria'], 'one')
        self.fields['deporte'] = adicionarClase(self.fields['deporte'], 'one')
        self.fields['objetivo'].widget.attrs['rows'] = 3
        self.fields['deporte'].queryset = TipoDisciplinaDeportiva.objects.all().order_by('descripcion')
        if deporte_id:
            self.fields['categoria'].queryset = CategoriaDisciplinaDeportiva.objects.filter(deporte=deporte_id).order_by('nombre')
            self.fields['modalidad'].queryset = ModalidadDisciplinaDeportiva.objects.filter(deporte=deporte_id).order_by('nombre')

    def clean(self):
        fecha_comienzo = self.cleaned_data['fecha_inicio']
        fecha_fin = self.cleaned_data['fecha_finalizacion']
        if fecha_fin < fecha_comienzo:
            msg = "La fecha de finalización es menor a la fecha de comienzo"
            self.add_error('fecha_inicio', msg)
            self.add_error('fecha_finalizacion', msg)

    class Meta:
        model = CalendarioNacional
        exclude = ('estado','entidad',)
        widgets = {
            'fecha_inicio': MyDateTimeWidget(),
            'fecha_finalizacion': MyDateTimeWidget(),
        }