# -*- encoding: utf-8 -*-
from django.forms import *
from django import forms
from entidades.models import *
from coldeportes.utilities import adicionarClase, MyDateWidget
# ----------------------------------------------------- Tenant ----------------------------------------------------------

class LigaForm(forms.ModelForm):
    required_css_class = 'required'
    pagina = forms.CharField(label="URL dentro del SIND", required=True)

    def __init__(self, *args, **kwargs):
        instancia = kwargs.get('instance', None)
        super(LigaForm, self).__init__(*args, **kwargs)
        self.fields['pagina'] = adicionarClase(self.fields['pagina'], 'form-control')
        self.fields['ciudad'] = adicionarClase(self.fields['ciudad'], 'one')
        self.fields['disciplina'] = adicionarClase(self.fields['disciplina'], 'one')
        self.fields['federacion'] = adicionarClase(self.fields['federacion'], 'one')

        if instancia != None:
            del self.fields['pagina']

    def clean(self):
        federacion = self.cleaned_data['federacion']
        disciplina = self.cleaned_data['disciplina']
        if federacion != None:
            if federacion.disciplina != disciplina:
                raise forms.ValidationError('La disciplina de la federación asociada no es la misma que la de la liga')
        
        return self.cleaned_data
    
    class Meta:
        model = Liga
        exclude = ('schema_name', 'domain_url', 'tipo', 'actores',)
        fields = ('nombre', 'pagina', 'pagina_web', 'ciudad', 'disciplina', 'federacion', 'direccion', 'telefono', 'descripcion', "resolucion", "fecha_resolucion", "fecha_vencimiento", "archivo",)
        widgets = {
            'fecha_resolucion': MyDateWidget(),
            'fecha_vencimiento': MyDateWidget(),
        }

class FederacionForm(forms.ModelForm):
    required_css_class = 'required'
    pagina = forms.CharField(label="URL dentro del SIND", required=True)

    def __init__(self, *args, **kwargs):
        instancia = kwargs.get('instance', None)
        super(FederacionForm, self).__init__(*args, **kwargs)
        self.fields['pagina'] = adicionarClase(self.fields['pagina'], 'form-control')
        self.fields['ciudad'] = adicionarClase(self.fields['ciudad'], 'one')
        self.fields['disciplina'] = adicionarClase(self.fields['disciplina'], 'one')

        if instancia != None:
            del self.fields['pagina']
    
    class Meta:
        model = Federacion
        exclude = ('schema_name', 'domain_url', 'tipo', 'actores','comite',)
        fields = ('nombre', 'pagina', 'pagina_web', 'ciudad', 'disciplina', 'direccion', 'telefono', 'descripcion', "resolucion", "fecha_resolucion", "fecha_vencimiento", "archivo",)
        widgets = {
            'fecha_resolucion': MyDateWidget(),
            'fecha_vencimiento': MyDateWidget(),
        }

class ClubForm(forms.ModelForm):
    required_css_class = 'required'
    pagina = forms.CharField(label="URL dentro del SIND", required=True)

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
        exclude = ('schema_name', 'domain_url', 'tipo', 'actores',)
        fields = ('nombre', 'pagina', 'pagina_web', 'ciudad', 'liga', 'direccion', 'telefono', 'descripcion', "resolucion", "fecha_resolucion", "fecha_vencimiento", "archivo",)
        widgets = {
            'fecha_resolucion': MyDateWidget(),
            'fecha_vencimiento': MyDateWidget(),
        }

class CajaDeCompensacionForm(forms.ModelForm):
    required_css_class = 'required'
    pagina = forms.CharField(label="URL dentro del SIND", required=True)

    def __init__(self, *args, **kwargs):
        instancia = kwargs.get('instance', None)
        super(CajaDeCompensacionForm, self).__init__(*args, **kwargs)
        self.fields['pagina'] = adicionarClase(self.fields['pagina'], 'form-control')
        self.fields['ciudad'] = adicionarClase(self.fields['ciudad'], 'one')

        if instancia != None:
            del self.fields['pagina']
    
    class Meta:
        model = CajaDeCompensacion
        exclude = ('schema_name', 'domain_url', 'tipo', 'actores',)
        fields = ('nombre', 'pagina', 'pagina_web', 'ciudad', 'direccion', 'telefono', 'descripcion',)

class EnteForm(forms.ModelForm):
    required_css_class = 'required'
    pagina = forms.CharField(label="URL dentro del SIND", required=True)

    def __init__(self, *args, **kwargs):
        instancia = kwargs.get('instance', None)
        super(EnteForm, self).__init__(*args, **kwargs)
        self.fields['pagina'] = adicionarClase(self.fields['pagina'], 'form-control')
        self.fields['ciudad'] = adicionarClase(self.fields['ciudad'], 'one')

        if instancia != None:
            del self.fields['pagina']

    class Meta:
        model = Ente
        exclude = ('schema_name', 'domain_url', 'tipo', 'actores', 'tipo_ente',)
        fields = ('nombre', 'pagina', 'pagina_web', 'ciudad', 'direccion', 'telefono', 'descripcion',)

class ComiteForm(forms.ModelForm):
    required_css_class = 'required'
    pagina = forms.CharField(label="Entidad", required=True)

    def __init__(self, *args, **kwargs):
        instancia = kwargs.get('instance', None)
        super(ComiteForm, self).__init__(*args, **kwargs)
        self.fields['pagina'] = adicionarClase(self.fields['pagina'], 'form-control')
        self.fields['ciudad'] = adicionarClase(self.fields['ciudad'], 'one')

        if instancia != None:
            del self.fields['pagina']

    class Meta:
        model = Comite
        exclude = ('schema_name', 'domain_url', 'tipo', 'actores', 'tipo_comite',)
        fields = ('nombre', 'pagina', 'pagina_web', 'ciudad', 'direccion', 'telefono', 'descripcion',)

class FederacionParalimpicaForm(forms.ModelForm):
    required_css_class = 'required'
    pagina = forms.CharField(label="Entidad", required=True)

    def __init__(self, *args, **kwargs):
        instancia = kwargs.get('instance', None)
        super(FederacionParalimpicaForm, self).__init__(*args, **kwargs)
        self.fields['pagina'] = adicionarClase(self.fields['pagina'], 'form-control')
        self.fields['discapacidad'] = adicionarClase(self.fields['discapacidad'], 'one')
        self.fields['ciudad'] = adicionarClase(self.fields['ciudad'], 'one')

        if instancia != None:
            del self.fields['pagina']

    class Meta:
        model = FederacionParalimpica
        exclude = ('schema_name', 'domain_url', 'tipo', 'actores','comite',)
        fields = ('nombre', 'pagina', 'pagina_web', 'ciudad', 'discapacidad', 'direccion', 'telefono', 'descripcion', "resolucion", "fecha_resolucion", "fecha_vencimiento", "archivo",)
        widgets = {
            'fecha_resolucion': MyDateWidget(),
            'fecha_vencimiento': MyDateWidget(),
        }


class LigaParalimpicaForm(forms.ModelForm):
    required_css_class = 'required'
    pagina = forms.CharField(label="Entidad", required=True)

    def __init__(self, *args, **kwargs):
        instancia = kwargs.get('instance', None)
        super(LigaParalimpicaForm, self).__init__(*args, **kwargs)
        self.fields['pagina'] = adicionarClase(self.fields['pagina'], 'form-control')
        self.fields['ciudad'] = adicionarClase(self.fields['ciudad'], 'one')
        self.fields['discapacidad'] = adicionarClase(self.fields['discapacidad'], 'one')

        if instancia != None:
            del self.fields['pagina']

    def clean(self):
        federacion = self.cleaned_data['federacion']
        discapacidad = self.cleaned_data['discapacidad']
        if federacion != None:
            if federacion.discapacidad != discapacidad:
                raise forms.ValidationError('La discapacidad de la federación asociada no es la misma que la de la liga')

        return self.cleaned_data

    class Meta:
        model = LigaParalimpica
        exclude = ('schema_name', 'domain_url', 'tipo', 'actores',)
        fields = ('nombre', 'pagina', 'pagina_web', 'ciudad', 'discapacidad', 'federacion', 'direccion', 'telefono', 'descripcion', 'resolucion', 'fecha_resolucion', 'fecha_vencimiento', 'archivo',)
        widgets = {
            'fecha_resolucion': MyDateWidget(),
            'fecha_vencimiento': MyDateWidget(),
        }

class ClubParalimpicoForm(forms.ModelForm):
    required_css_class = 'required'
    pagina = forms.CharField(label="URL dentro del SIND", required=True)

    def __init__(self, *args, **kwargs):
        instancia = kwargs.get('instance', None)
        super(ClubParalimpicoForm, self).__init__(*args, **kwargs)
        self.fields['pagina'] = adicionarClase(self.fields['pagina'], 'form-control')
        self.fields['ciudad'] = adicionarClase(self.fields['ciudad'], 'one')
        self.fields['liga'] = adicionarClase(self.fields['liga'], 'one')

        if instancia != None:
            del self.fields['pagina']
    
    class Meta:
        model = ClubParalimpico
        exclude = ('schema_name', 'domain_url', 'tipo', 'actores',)
        fields = ('nombre', 'pagina', 'pagina_web', 'ciudad', 'liga', 'direccion', 'telefono', 'descripcion', 'resolucion', 'fecha_resolucion', 'fecha_vencimiento', 'archivo',)
        widgets = {
            'fecha_resolucion': MyDateWidget(),
            'fecha_vencimiento': MyDateWidget(),
        }

class CafForm(forms.ModelForm):
    required_css_class = 'required'
    pagina = forms.CharField(label="URL dentro del SIND", required=True)

    def __init__(self, *args, **kwargs):
        instancia = kwargs.get('instance', None)
        super(CafForm, self).__init__(*args, **kwargs)
        self.fields['pagina'] = adicionarClase(self.fields['pagina'], 'form-control')
        self.fields['ciudad'] = adicionarClase(self.fields['ciudad'], 'one')

        if instancia != None:
            del self.fields['pagina']
    
    class Meta:
        model = Caf
        exclude = ('schema_name', 'domain_url', 'tipo', 'actores',)
        fields = ('nombre', 'pagina', 'pagina_web', 'ciudad', 'direccion', 'telefono', 'descripcion',)


class EscuelaDeportivaForm(forms.ModelForm):
    required_css_class = 'required'
    pagina = forms.CharField(label="URL dentro del SIND", required=True)

    def __init__(self, *args, **kwargs):
        instancia = kwargs.get('instance', None)
        super(EscuelaDeportivaForm, self).__init__(*args, **kwargs)
        self.fields['pagina'] = adicionarClase(self.fields['pagina'], 'form-control')
        self.fields['ciudad'] = adicionarClase(self.fields['ciudad'], 'one')
        self.fields['disciplina'] = adicionarClase(self.fields['disciplina'], 'one')

        if instancia != None:
            del self.fields['pagina']
    
    class Meta:
        model = EscuelaDeportiva_
        exclude = ('schema_name', 'domain_url', 'tipo', 'actores',)
        fields = ('nombre', 'pagina', 'pagina_web', 'disciplina', 'ciudad', 'direccion', 'telefono', 'descripcion',)


# --------------------------------------------------- Fin Tenant ---------------------------------------------------------

class ActoresForm(forms.ModelForm):


    #estos son los actores que se pueden o no tener por tanto son seleccionables
    ACTORES = {
        '1': [],#Liga
        '2': ['escenarios'],#Federacion
        '3': ['centros','escenarios','deportistas'],#Club
        '4': ['escenarios'],#CajaDeCompensacion
        '5': ['escenarios','centros_biomedicos'],#Ente
        '6': [],#Comite
        '7': [],#FederacionParalimpica
        '8': ['deportistas'],#LigaParalimpica
        '9': ['centros','escenarios'],#clubParalimpico
        '10': ['escenarios'],#Caf
        '11': ['escenarios']#EscuelaDeportiva_
    }

    def __init__(self, *args, **kwargs):
        tipo = kwargs.pop('tipo', None)
        tipoEnte = kwargs.pop('tipoEnte', None)#no se está usando
        super(ActoresForm, self).__init__(*args, **kwargs)
        if tipo:
            self.quitar_campos(self.get_campos_quitar(self.ACTORES[tipo]))

    def quitar_campos(self,campos):
        for campo in campos:
            del self.fields[campo]

    def get_campos_quitar(self,campos):
        all_campos = ['centros','escenarios','deportistas','personal_apoyo','dirigentes','cajas','selecciones','centros_biomedicos','normas','escuelas_deportivas','noticias']
        for campo in campos:
            try:
                del all_campos[all_campos.index(campo)]
            except ValueError:
                pass
        return (all_campos)

    class Meta:
        model = Actores
        #exclude = ()
        fields = '__all__'