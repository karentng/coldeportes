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


'''class PermisosForm(forms.Form):
    ACTORES = (
        ('no_tiene', '--'),
        ('obligatorio', 'O'),
        ('puede_tener', 'X'),
        ('puede_tener_lectura', 'X %'),
        ('no_tiene_lectura','-- %'),
    )

    class Meta:
        model = Permisos
        exclude = ('entidad',)
    
    ente_municipal_centros = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    ente_municipal_escenarios = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    ente_municipal_deportistas = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    ente_municipal_personal = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    ente_municipal_dirigentes = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    ente_municipal_cajas = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    ente_municipal_selecciones = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    ente_municipal_biomedicos = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    ente_municipal_normograma = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    ente_municipal_escuela = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    ente_municipal_noticias = forms.ChoiceField(choices=ACTORES,initial='1', required = True)

    ente_departamental_centros = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    ente_departamental_escenarios = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    ente_departamental_deportistas = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    ente_departamental_personal = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    ente_departamental_dirigentes = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    ente_departamental_cajas = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    ente_departamental_selecciones = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    ente_departamental_biomedicos = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    ente_departamental_normograma = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    ente_departamental_escuela = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    ente_departamental_noticias = forms.ChoiceField(choices=ACTORES,initial='1', required = True)

    coc_centros = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    coc_escenarios = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    coc_deportistas = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    coc_personal = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    coc_dirigentes = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    coc_cajas = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    coc_selecciones = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    coc_biomedicos = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    coc_normograma = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    coc_escuela = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    coc_noticias = forms.ChoiceField(choices=ACTORES,initial='1', required = True)

    federacion_centros = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    federacion_escenarios = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    federacion_deportistas = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    federacion_personal = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    federacion_dirigentes = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    federacion_cajas = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    federacion_selecciones = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    federacion_biomedicos = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    federacion_normograma = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    federacion_escuela = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    federacion_noticias = forms.ChoiceField(choices=ACTORES,initial='1', required = True)

    liga_centros = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    liga_escenarios = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    liga_deportistas = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    liga_personal = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    liga_dirigentes = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    liga_cajas = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    liga_selecciones = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    liga_biomedicos = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    liga_normograma = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    liga_escuela = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    liga_noticias = forms.ChoiceField(choices=ACTORES,initial='1', required = True)

    club_centros = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    club_escenarios = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    club_deportistas = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    club_personal = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    club_dirigentes = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    club_cajas = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    club_selecciones = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    club_biomedicos = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    club_normograma = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    club_escuela = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    club_noticias = forms.ChoiceField(choices=ACTORES,initial='1', required = True)

    cpc_centros = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    cpc_escenarios = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    cpc_deportistas = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    cpc_personal = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    cpc_dirigentes = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    cpc_cajas = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    cpc_selecciones = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    cpc_biomedicos = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    cpc_normograma = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    cpc_escuela = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    cpc_noticias = forms.ChoiceField(choices=ACTORES,initial='1', required = True)

    federacionpara_centros = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    federacionpara_escenarios = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    federacionpara_deportistas = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    federacionpara_personal = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    federacionpara_dirigentes = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    federacionpara_cajas = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    federacionpara_selecciones = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    federacionpara_biomedicos = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    federacionpara_normograma = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    federacionpara_escuela = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    federacionpara_noticias = forms.ChoiceField(choices=ACTORES,initial='1', required = True)

    ligapara_centros = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    ligapara_escenarios = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    ligapara_deportistas = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    ligapara_personal = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    ligapara_dirigentes = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    ligapara_cajas = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    ligapara_selecciones = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    ligapara_biomedicos = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    ligapara_normograma = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    ligapara_escuela = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    ligapara_noticias = forms.ChoiceField(choices=ACTORES,initial='1', required = True)

    clubpara_centros = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    clubpara_escenarios = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    clubpara_deportistas = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    clubpara_personal = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    clubpara_dirigentes = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    clubpara_cajas = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    clubpara_selecciones = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    clubpara_biomedicos = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    clubpara_normograma = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    clubpara_escuela = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    clubpara_noticias = forms.ChoiceField(choices=ACTORES,initial='1', required = True)

    cajas_centros = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    cajas_escenarios = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    cajas_deportistas = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    cajas_personal = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    cajas_dirigentes = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    cajas_cajas = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    cajas_selecciones = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    cajas_biomedicos = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    cajas_normograma = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    cajas_escuela = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    cajas_noticias = forms.ChoiceField(choices=ACTORES,initial='1', required = True)

    caf_centros = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    caf_escenarios = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    caf_deportistas = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    caf_personal = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    caf_dirigentes = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    caf_cajas = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    caf_selecciones = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    caf_biomedicos = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    caf_normograma = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    caf_escuela = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    caf_noticias = forms.ChoiceField(choices=ACTORES,initial='1', required = True)

    escuelas_centros = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    escuelas_escenarios = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    escuelas_deportistas = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    escuelas_personal = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    escuelas_dirigentes = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    escuelas_cajas = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    escuelas_selecciones = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    escuelas_biomedicos = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    escuelas_normograma = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    escuelas_escuela = forms.ChoiceField(choices=ACTORES,initial='1', required = True)
    escuelas_noticias = forms.ChoiceField(choices=ACTORES,initial='1', required = True)'''