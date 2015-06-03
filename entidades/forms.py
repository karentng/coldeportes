# -*- encoding: utf-8 -*-
from django.forms import *
from django import forms
from entidades.models import *

class EntidadForm(forms.ModelForm):
	class Meta:
		model = Entidad
		exclude = ()