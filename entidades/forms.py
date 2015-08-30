# -*- encoding: utf-8 -*-
from django.forms import *
from django import forms
from entidades.models import *
from coldeportes.utilities import adicionarClase

# ----------------------------------------------------- Tenant ----------------------------------------------------------

class LigaForm(forms.ModelForm):
    pagina = forms.CharField(label="Página Web")

    def __init__(self, *args, **kwargs):
        instancia = kwargs.get('instance', None)
        super(LigaForm, self).__init__(*args, **kwargs)
        self.fields['pagina'] = adicionarClase(self.fields['pagina'], 'form-control')
        self.fields['departamento'] = adicionarClase(self.fields['departamento'], 'one')
        self.fields['disciplina'] = adicionarClase(self.fields['disciplina'], 'one')

        if instancia != None:
            del self.fields['pagina']
    
    class Meta:
        model = Liga
        exclude = ('schema_name', 'domain_url', 'tipo', 'actores',)
        fields = ('nombre', 'pagina', 'pagina_web', 'departamento', 'disciplina', 'federacion', 'direccion', 'telefono', 'descripcion',)

class FederacionForm(forms.ModelForm):
    pagina = forms.CharField(label="Página Web")

    def __init__(self, *args, **kwargs):
        instancia = kwargs.get('instance', None)
        super(FederacionForm, self).__init__(*args, **kwargs)
        self.fields['pagina'] = adicionarClase(self.fields['pagina'], 'form-control')

        if instancia != None:
            del self.fields['pagina']
    
    class Meta:
        model = Federacion
        exclude = ('schema_name', 'domain_url', 'tipo', 'actores', 'federacion',)
        fields = ('nombre', 'pagina', 'pagina_web', 'disciplina', 'direccion', 'telefono', 'descripcion',)

class ClubForm(forms.ModelForm):
    pagina = forms.CharField(label="Página Web")

    def __init__(self, *args, **kwargs):
        instancia = kwargs.get('instance', None)
        super(ClubForm, self).__init__(*args, **kwargs)
        self.fields['pagina'] = adicionarClase(self.fields['pagina'], 'form-control')
        self.fields['ciudad'] = adicionarClase(self.fields['ciudad'], 'one')
        self.fields['liga'] = adicionarClase(self.fields['liga'], 'one')

        if instancia != None:
            del self.fields['pagina']
    
    class Meta:
        model = Club
        exclude = ('schema_name', 'domain_url', 'tipo', 'actores', 'federacion',)
        fields = ('nombre', 'pagina', 'pagina_web', 'ciudad', 'liga', 'direccion', 'telefono', 'descripcion',)

class CajaDeCompensacionForm(forms.ModelForm):
    pagina = forms.CharField(label="Página Web")

    def __init__(self, *args, **kwargs):
        instancia = kwargs.get('instance', None)
        super(CajaDeCompensacionForm, self).__init__(*args, **kwargs)
        self.fields['pagina'] = adicionarClase(self.fields['pagina'], 'form-control')
        self.fields['ciudad'] = adicionarClase(self.fields['ciudad'], 'one')

        if instancia != None:
            del self.fields['pagina']
    
    class Meta:
        model = CajaDeCompensacion
        exclude = ('schema_name', 'domain_url', 'tipo', 'actores', 'federacion',)
        fields = ('nombre', 'pagina', 'pagina_web', 'ciudad', 'direccion', 'telefono', 'descripcion',)

class EnteForm(forms.ModelForm):
    pagina = forms.CharField(label="Página Web")

    def __init__(self, *args, **kwargs):
        instancia = kwargs.get('instance', None)
        super(EnteForm, self).__init__(*args, **kwargs)
        self.fields['pagina'] = adicionarClase(self.fields['pagina'], 'form-control')

        if instancia != None:
            del self.fields['pagina']

    class Meta:
        model = Ente
        exclude = ('schema_name', 'domain_url', 'tipo', 'actores', 'federacion',)
        fields = ('nombre', 'tipo_ente', 'pagina', 'pagina_web', 'ciudad', 'direccion', 'telefono', 'descripcion',)

# --------------------------------------------------- Fin Tenant ---------------------------------------------------------

class ActoresForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        tipo = kwargs.pop('tipo', None)
        super(ActoresForm, self).__init__(*args, **kwargs)

        if tipo == '1':
            #Liga
            del self.fields['centros']
            del self.fields['escenarios']
            del self.fields['deportistas']
            del self.fields['cajas']
        elif tipo == '2':
            #Federacion
            del self.fields['centros']
            del self.fields['escenarios']
            del self.fields['deportistas']
            del self.fields['cajas']
        elif tipo == '3':
            #Club
            del self.fields['cajas']
        elif tipo == '4':
            #CajaDeCompensacion
            self.fields['cajas'].widget = forms.HiddenInput()
            del self.fields['centros']
            del self.fields['deportistas']
            del self.fields['dirigentes']
        elif tipo == '5':
            #Ente
            pass

    class Meta:
        model = Actores
        exclude = ()