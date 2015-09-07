from django import forms
from django.forms import ModelForm
from normograma.models import *
from coldeportes.utilities import adicionarClase

class NormaForm(forms.ModelForm):
	class Meta:
		model = Norma