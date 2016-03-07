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
        cleaned_data = super(LigaForm, self).clean()
        federacion = cleaned_data['federacion']
        disciplina = cleaned_data['disciplina']
        if federacion != None:
            if federacion.disciplina != disciplina:
                raise forms.ValidationError('La disciplina de la federación asociada no es la misma que la de la liga', code='invalid_disciplina')
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
        self.fields['disciplina'] = adicionarClase(self.fields['disciplina'], 'one')
        self.fields['tipo_club'] = adicionarClase(self.fields['tipo_club'], 'one')

        if instancia != None:
            del self.fields['pagina']

    def clean(self):
        cleaned_data = super(ClubForm, self).clean()
        liga = cleaned_data['liga']
        disciplina = cleaned_data['disciplina']
        if liga != None:
            if liga.disciplina != disciplina:
                raise forms.ValidationError('La disciplina de la liga asociada no es la misma que la del club', code='invalid_disciplina')
        return self.cleaned_data

    class Meta:
        model = Club
        exclude = ('schema_name', 'domain_url', 'tipo', 'actores',)
        fields = ('nombre', 'tipo_club', 'pagina', 'pagina_web', 'ciudad', 'disciplina','liga', 'direccion', 'telefono', 'descripcion', "resolucion", "fecha_resolucion", "fecha_vencimiento", "archivo",)
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
        cleaned_data = super(LigaParalimpicaForm, self).clean()
        federacion = cleaned_data['federacion']
        discapacidad = cleaned_data['discapacidad']
        if federacion != None:
            if federacion.discapacidad != discapacidad:
                raise forms.ValidationError('La discapacidad de la federación asociada no es la misma que la de la liga', code='invalid_discapacidad')
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
        self.fields['disciplinas'] = adicionarClase(self.fields['disciplinas'],'many')

        if instancia != None:
            del self.fields['pagina']

    def clean(self):
        cleaned_data = super(ClubParalimpicoForm, self).clean()
        liga = cleaned_data['liga']
        discapacidad = cleaned_data['discapacidad']
        if liga != None:
            if liga.discapacidad != discapacidad:
                raise forms.ValidationError('La discapacidad de la liga asociada no es la misma que la del club', code='invalid_discapacidad')
        return self.cleaned_data

    class Meta:
        model = ClubParalimpico
        exclude = ('schema_name', 'domain_url', 'tipo', 'actores',)
        fields = ('nombre', 'pagina', 'pagina_web', 'ciudad', 'discapacidad','liga', 'direccion', 'telefono', 'descripcion', 'resolucion', 'fecha_resolucion', 'fecha_vencimiento', 'archivo','disciplinas',)
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

class PermisosForm(forms.ModelForm):

    ENTIDAD = (
        ([5,1], 'Ente municipal'),
        ([5,2], 'Ente departamental'),
        ([6,1], 'Comité Olímpico Colombiano'),
        ([2,0], 'Federación'),
        ([1,0], 'Liga'),
        ([3,0], 'Club'),
        ([6,2], 'Comité Paralímpico Colombiano'),
        ([7,0], 'Federación Paralimpica'),
        ([8,0], 'Liga Paralimpica'),
        ([9,0], 'Club Paralimpico'),
        ([4,0], 'Cajas de Compensación'),
        ([10,0], 'Centro de Acondicionamiento'),
        ([11,0], 'Escuela de Formación Deportiva'),
    )

    entidades = forms.ChoiceField(choices=ENTIDAD)

    def __init__(self, *args, **kwargs):
        super(PermisosForm, self).__init__(*args, **kwargs)
        if self.instance.entidad:
            self.fields['entidades'].initial = [self.instance.entidad,self.instance.tipo]

    class Meta:
        model = Permisos
        exclude = ('entidad','tipo')

#####TEMPORAL REGISTRO DE MODALIDADES Y CATEOGORIAS####
class ModalidadForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(ModalidadForm, self).__init__(*args, **kwargs)
        self.fields['deporte'] = adicionarClase(self.fields['deporte'], 'one')

    class Meta:
        model = ModalidadDisciplinaDeportiva
        exclude = ('',)

class CategoriaForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(CategoriaForm, self).__init__(*args, **kwargs)
        self.fields['deporte'] = adicionarClase(self.fields['deporte'], 'one')

    class Meta:
        model = CategoriaDisciplinaDeportiva
        exclude = ('',)

class DeporteForm(ModelForm):

    class Meta:
        model = TipoDisciplinaDeportiva
        exclude = ('',)

class SocioClubForm(ModelForm):
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        super(SocioClubForm, self).__init__(*args, **kwargs)
        if self.instance.pk != None:
            self.fields['tipo_documento'].widget.attrs['readonly'] = 1
            self.fields['numero_documento'].widget.attrs['readonly'] = 1

    class Meta:
        model = SocioClub
        exclude = ('estado','club_id')
        
        
#Formulario Planes de Costo de un club.
#Autor: Yalile Bermudes
#Fecha: 02/03/2016
class PlanDeCostoForm(ModelForm):
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        super(PlanDeCostoForm, self).__init__(*args, **kwargs)
        self.fields['precio'].widget.attrs.update({'min':0})

    class Meta:
        model = PlanesDeCostoClub
        exclude = ('estado', )
