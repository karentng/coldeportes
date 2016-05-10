# -*- encoding: utf-8 -*-
import datetime
from django import forms
from registro_resultados.models import *
from coldeportes.utilities import adicionarClase, MyDateWidget
from reportes.utilities import add_visualizacion
from django.core.exceptions import ValidationError

class JuegoForm(forms.ModelForm):

    required_css_class = 'required'
    
    def __init__(self, *args, **kwargs):
        super(JuegoForm, self).__init__(*args, **kwargs)
        self.fields['pais'] = adicionarClase(self.fields['pais'], 'one')
        self.fields['descripcion'].widget.attrs['rows'] = 3

    class Meta:
        model = Juego
        exclude = ()


class CompetenciaForm(forms.ModelForm):

    required_css_class = 'required'

    TIPOS_REGISTROS = (
        (1, "Tiempos"),
        (2, "Puntos"),
        (3, "Metros"),
    )

    tipo_registro = forms.ChoiceField(widget=forms.RadioSelect, choices=TIPOS_REGISTROS, label='Registros De Competencia')

    def __init__(self, *args, **kwargs):

        deporte_id = kwargs.pop('deporte_id',None)
        super(CompetenciaForm, self).__init__(*args, **kwargs)
        self.fields['deporte'] = adicionarClase(self.fields['deporte'], 'one')
        self.fields['deporte'].queryset = TipoDisciplinaDeportiva.objects.all().order_by('descripcion')
        self.fields['descripcion'].widget.attrs['rows'] = 3

        if deporte_id:
            self.fields['categoria'].queryset = CategoriaDisciplinaDeportiva.objects.filter(deporte=deporte_id).order_by('nombre')
            self.fields['modalidad'].queryset = ModalidadDisciplinaDeportiva.objects.filter(deporte=deporte_id).order_by('nombre')

    class Meta:
        model = Competencia
        exclude = ('juego',)
        widgets = {
            'fecha_competencia': MyDateWidget(),
        }


class CompetenciaEditarForm(forms.ModelForm):

    required_css_class = 'required'

    def __init__(self, *args, **kwargs):

        deporte_id = kwargs.pop('deporte_id',None)
        super(CompetenciaEditarForm, self).__init__(*args, **kwargs)
        self.fields['deporte'] = adicionarClase(self.fields['deporte'], 'one')
        self.fields['deporte'].queryset = TipoDisciplinaDeportiva.objects.all().order_by('descripcion')
        self.fields['descripcion'].widget.attrs['rows'] = 3

        if deporte_id:
            self.fields['categoria'].queryset = CategoriaDisciplinaDeportiva.objects.filter(deporte=deporte_id).order_by('nombre')
            self.fields['modalidad'].queryset = ModalidadDisciplinaDeportiva.objects.filter(deporte=deporte_id).order_by('nombre')

    class Meta:
        model = Competencia
        exclude = ('juego', 'tipo_registro','tipos_participantes')
        widgets = {
            'fecha_competencia': MyDateWidget(),
        }


class ParticipanteTiempoForm(forms.ModelForm):

    required_css_class = 'required'

    def __init__(self, *args, **kwargs):

        competencia = kwargs.pop('competencia')
        super(ParticipanteTiempoForm, self).__init__(*args, **kwargs)
        self.fields['departamento'] = adicionarClase(self.fields['departamento'], 'one')
    
    def clean_marca(self):

        marca = self.cleaned_data['marca']
        if marca:
            try:
                if marca.isdigit() or "." in marca or ":" in marca:
                    return self.cleaned_data['marca']
                else:
                    raise ValidationError('La marca debe tener números, puntos y/o dos puntos. Ej: 24.100, 03:05')
            except:
                raise ValidationError('La marca debe tener números, puntos y/o dos puntos. Ej: 24.100, 03:05')
        else:
            pass

    def clean_fecha_nacimiento(self):

        fecha = self.cleaned_data['fecha_nacimiento']
        if fecha:            
            if fecha >= datetime.date.today():
                raise ValidationError('La fecha de nacimiento no puede ser mayor o igual a la actual.')
            else:
                return self.cleaned_data['fecha_nacimiento']
        else:
            pass

    def clean_tiempo(self):

        tiempo = self.cleaned_data['tiempo']
        if tiempo:
            try:
                if tiempo.isdigit() or "." in tiempo or ":" in tiempo:
                    return self.cleaned_data['tiempo']
                else:
                    raise ValidationError('El tiempo debe tener números, puntos y/o dos puntos. Ej: 24.100, 03:05.102')
            except:
                raise ValidationError('El tiempo debe tener números, puntos y/o dos puntos. Ej: 24.100, 03:05.102')
        pass
    
    class Meta:

        model = Participante
        exclude = ("competencia", 'puntos', 'equipo', 'metros')
        widgets = {
            'fecha_nacimiento': MyDateWidget(),
        }


class ParticipantePuntosForm(forms.ModelForm):

    required_css_class = 'required'

    def __init__(self, *args, **kwargs):

        competencia = kwargs.pop('competencia')
        super(ParticipantePuntosForm, self).__init__(*args, **kwargs)
        self.fields['departamento'] = adicionarClase(self.fields['departamento'], 'one')
    
    class Meta:

        model = Participante
        exclude = ("competencia", 'tiempo', 'marca', 'equipo', 'metros')
        widgets = {
            'fecha_nacimiento': MyDateWidget(),
        }

    def clean_fecha_nacimiento(self):

        fecha = self.cleaned_data['fecha_nacimiento']
        if fecha:            
            if fecha >= datetime.date.today():
                raise ValidationError('La fecha de nacimiento no puede ser mayor o igual a la actual.')
            else:
                return self.cleaned_data['fecha_nacimiento']
        else:
            pass

class ParticipanteMetrosForm(forms.ModelForm):

    required_css_class = 'required'

    def __init__(self, *args, **kwargs):

        competencia = kwargs.pop('competencia')
        super(ParticipanteMetrosForm, self).__init__(*args, **kwargs)
        self.fields['departamento'] = adicionarClase(self.fields['departamento'], 'one')

    def clean_marca(self):

        marca = self.cleaned_data['marca']
        if marca:
            try:
                if marca.isdigit() or "." in marca or ":" in marca:
                    return self.cleaned_data['marca']
                else:
                    raise ValidationError('La marca debe tener números, puntos y/o dos puntos. Ej: 24.100, 03:05')
            except:
                raise ValidationError('La marca debe tener números, puntos y/o dos puntos. Ej: 24.100, 03:05')
        else:
            pass
            
    class Meta:

        model = Participante
        exclude = ("competencia", 'tiempo', 'equipo', 'puntos')
        widgets = {
            'fecha_nacimiento': MyDateWidget(),
        }

    def clean_fecha_nacimiento(self):

        fecha = self.cleaned_data['fecha_nacimiento']
        if fecha:            
            if fecha >= datetime.date.today():
                raise ValidationError('La fecha de nacimiento no puede ser mayor o igual a la actual.')
            else:
                return self.cleaned_data['fecha_nacimiento']
        else:
            pass

class ParticipanteEquipoForm(forms.ModelForm):

    required_css_class = 'required'
    
    def __init__(self, *args, **kwargs):

        competencia = kwargs.pop('competencia')
        super(ParticipanteEquipoForm, self).__init__(*args, **kwargs)
        self.fields['departamento'] = adicionarClase(self.fields['departamento'], 'one')
    
    class Meta:

        model = Participante
        exclude = ("competencia", 'tiempo', 'marca', 'equipo', 'puntos', 'posicion', 'metros')
        widgets = {
            'fecha_nacimiento': MyDateWidget(),
        }

    def clean_fecha_nacimiento(self):

        fecha = self.cleaned_data['fecha_nacimiento']
        if fecha:            
            if fecha >= datetime.date.today():
                raise ValidationError('La fecha de nacimiento no puede ser mayor o igual a la actual.')
            else:
                return self.cleaned_data['fecha_nacimiento']
        else:
            pass


class EquipoTiempoForm(forms.ModelForm):

    required_css_class = 'required'

    def __init__(self, *args, **kwargs):

        super(EquipoTiempoForm, self).__init__(*args, **kwargs)
        self.fields['departamento'] = adicionarClase(self.fields['departamento'], 'one')

    def clean_marca(self):

        marca = self.cleaned_data['marca']
        if marca:
            try:
                if marca.isdigit() or "." in marca or ":" in marca:
                    return self.cleaned_data['marca']
                else:
                    raise ValidationError('La marca debe tener números, puntos y/o dos puntos. Ej: 24.100, 03:05')
            except:
                raise ValidationError('La marca debe tener números, puntos y/o dos puntos. Ej: 24.100, 03:05')
        else:
            pass

    def clean_tiempo(self):

        tiempo = self.cleaned_data['tiempo']
        if tiempo:
            try:
                if tiempo.isdigit() or "." in tiempo or ":" in tiempo:
                    return self.cleaned_data['tiempo']
                else:
                    raise ValidationError('El tiempo debe tener números, puntos y/o dos puntos. Ej: 24.100, 03:05.102')
            except:
                raise ValidationError('El tiempo debe tener números, puntos y/o dos puntos. Ej: 24.100, 03:05.102')
        pass
    

    class Meta:

        model = Equipo
        exclude = ("competencia", 'puntos', 'metros')


class EquipoPuntosForm(forms.ModelForm):

    required_css_class = 'required'

    def __init__(self, *args, **kwargs):

        super(EquipoPuntosForm, self).__init__(*args, **kwargs)
        self.fields['departamento'] = adicionarClase(self.fields['departamento'], 'one')

    class Meta:

        model = Equipo
        exclude = ("competencia", 'tiempo', 'marca', 'metros')


class EquipoMetrosForm(forms.ModelForm):

    required_css_class = 'required'

    def __init__(self, *args, **kwargs):

        super(EquipoMetrosForm, self).__init__(*args, **kwargs)
        self.fields['departamento'] = adicionarClase(self.fields['departamento'], 'one')

    class Meta:

        model = Equipo
        exclude = ("competencia", 'tiempo', 'puntos')

    def clean_marca(self):

        marca = self.cleaned_data['marca']
        if marca:
            try:
                if marca.isdigit() or "." in marca or ":" in marca:
                    return self.cleaned_data['marca']
                else:
                    raise ValidationError('La marca debe tener números, puntos y/o dos puntos. Ej: 24.100, 03:05')
            except:
                raise ValidationError('La marca debe tener números, puntos y/o dos puntos. Ej: 24.100, 03:05')
        else:
            pass

    
class CompetenciasBaseDeDatos(forms.Form):

    archivo = forms.FileField(label="Archivo de competencias")


class ParticipantesBaseDeDatos(forms.Form):
    archivo = forms.FileField(label="Archivo de participantes")


class FiltrosMedalleriaDeptGenForm(forms.Form):
    
    GENEROS = (
        (1,'Masculino'),
        (2,'Femenino'),
    )    
    juegos = forms.ModelChoiceField(queryset=Juego.objects.all(), required=False)
    departamentos = forms.ModelMultipleChoiceField(queryset=Departamento.objects.all(), required=False)
    generos = forms.MultipleChoiceField(label="Géneros", required=False, widget=forms.SelectMultiple(attrs={'placeholder': 'Género'}), choices=GENEROS)
    visualizacion = forms.ChoiceField(label="Visualización")

    def __init__(self, *args, **kwargs):

        visualizaciones_definidas = kwargs.pop('visualizaciones', None)
        eliminar = kwargs.pop('eliminar', None)
        super(FiltrosMedalleriaDeptGenForm, self).__init__(*args, **kwargs)
        self.fields['departamentos'] = adicionarClase(self.fields['departamentos'], 'many')
        self.fields['generos'] = adicionarClase(self.fields['generos'], 'many')
        self.fields['juegos'] = adicionarClase(self.fields['juegos'], 'one')
        add_visualizacion(self.fields['visualizacion'], visualizaciones_definidas)
        
        if eliminar:
            del self.fields[eliminar]

        add_visualizacion(self.fields['visualizacion'], visualizaciones_definidas)


class FiltrosTablaMedalleriaForm(forms.Form):

    juego = forms.ModelChoiceField(queryset=Juego.objects.all().order_by('anio'))
    deportes = forms.ModelMultipleChoiceField(queryset=TipoDisciplinaDeportiva.objects.all().order_by('descripcion'), required=False)

    def __init__(self, *args, **kwargs):
        
        super(FiltrosTablaMedalleriaForm, self).__init__(*args, **kwargs)
        self.fields['deportes'] = adicionarClase(self.fields['deportes'], 'many')
        self.fields['juego'] = adicionarClase(self.fields['juego'], 'one')

    
class ParticipantesBaseDeDatos(forms.Form):
    archivo = forms.FileField(label="Archivo de participantes")

