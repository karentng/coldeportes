from django.db import models
from snd.models import Deportista,ComposicionCorporal,HistorialDeportivo,InformacionAcademica,InformacionAdicional,HistorialLesiones
from rest_framework import serializers
from reportes.models import TenantDeportistaView
from entidades.modelos_vistas_reportes import PublicDeportistaView
from entidades.models import Ciudad,Nacionalidad,TipoDisciplinaDeportiva

# Create your models here.
class DeportistaSerializable(serializers.ModelSerializer):
    entidad = serializers.ReadOnlyField(source='entidad.schema_name')
    estado = serializers.ReadOnlyField(source='get_estado_display')
    nacionalidad = serializers.SlugRelatedField(many=True,queryset=Nacionalidad.objects.all(),slug_field='nombre')
    ciudad_residencia = serializers.SlugRelatedField(many=False, queryset=Ciudad.objects.all(), slug_field='nombre')
    disciplinas = serializers.SlugRelatedField(many=True, queryset=TipoDisciplinaDeportiva.objects.all(), slug_field='descripcion')

    class Meta:
        model = Deportista
        exclude = ('fecha_creacion',)

#Modelo para listado tenants tipo liga y federacion
class DeportistaListSerializable(serializers.ModelSerializer):
    entidad = serializers.ReadOnlyField(source='entidad.schema_name')
    estado = serializers.ReadOnlyField(source='get_estado_display')
    nacionalidad = serializers.SlugRelatedField(many=False, read_only=True, slug_field='nombre')
    ciudad_residencia = serializers.SlugRelatedField(many=False, read_only=True, slug_field='nombre')
    tipodisciplinadeportiva = serializers.SlugRelatedField(many=False, read_only=True,
                                               slug_field='descripcion')

    class Meta:
        model = TenantDeportistaView
        fields = ('id','nombres','apellidos','tipo_id','genero','identificacion','fecha_nacimiento','ciudad_residencia','barrio','comuna','email','telefono','direccion','lgtbi','entidad','estado','etnia','video','tipodisciplinadeportiva','nacionalidad','foto',)

#Modelo para tenant público
class DeportistasPublicSerializable(serializers.ModelSerializer):
    entidad = serializers.ReadOnlyField(source='entidad.schema_name')
    estado = serializers.ReadOnlyField(source='get_estado_display')
    nacionalidad = serializers.SlugRelatedField(many=False, read_only=True, slug_field='nombre')
    ciudad_residencia = serializers.SlugRelatedField(many=False, read_only=True, slug_field='nombre')
    tipodisciplinadeportiva = serializers.SlugRelatedField(many=False, read_only=True,
                                               slug_field='descripcion')

    class Meta:
        model = PublicDeportistaView
        fields = ('id','nombres','apellidos','tipo_id','genero','identificacion','fecha_nacimiento','ciudad_residencia','barrio','comuna','email','telefono','direccion','lgtbi','entidad','estado','etnia','video','tipodisciplinadeportiva','nacionalidad','foto',)

class ComposicionCorporalSerializable(serializers.ModelSerializer):
    entidad = serializers.ReadOnlyField(source='deportista.entidad.schema_name')

    def validate(self, data):
        """
        Permite validar que no se cambie la llave a deportista en actualizacion de datos
        :param data: Datos del serializador
        :return: datos validados
        """
        if self.context['request'].method in ['PUT', 'PATCH']:
            del data['deportista']
        return data

    class Meta:
        model = ComposicionCorporal
        exclude = ('fecha_creacion',)

class HistorialDeportivoSerializable(serializers.ModelSerializer):
    entidad = serializers.ReadOnlyField(source='deportista.entidad.schema_name')

    def validate(self, data):
        """
            Permite validar que no se cambie la llave a deportista en actualizacion de datos
            :param data: Datos del serializador
            :return: datos validados
            """
        if self.context['request'].method in ['PUT', 'PATCH']:
            del data['deportista']
        return data

    class Meta:
        model = HistorialDeportivo
        exclude = ('fecha_creacion',)

class InformacionAcademicaSerializable(serializers.ModelSerializer):
    entidad = serializers.ReadOnlyField(source='deportista.entidad.schema_name')

    def validate(self, data):
        """
            Permite validar que no se cambie la llave a deportista en actualizacion de datos
            :param data: Datos del serializador
            :return: datos validados
            """
        if self.context['request'].method in ['PUT', 'PATCH']:
            del data['deportista']
        return data

    class Meta:
        model = InformacionAcademica
        exclude = ('fecha_creacion',)

class InformacionAdicionalSerializable(serializers.ModelSerializer):
    entidad = serializers.ReadOnlyField(source='deportista.entidad.schema_name')

    def validate(self, data):
        """
            Permite validar que no se cambie la llave a deportista en actualizacion de datos
            :param data: Datos del serializador
            :return: datos validados
            """
        if self.context['request'].method in ['PUT', 'PATCH']:
            del data['deportista']
        return data

    class Meta:
        model = InformacionAdicional
        exclude = ('fecha_creacion',)

class HistorialLesionesSerializable(serializers.ModelSerializer):
    entidad = serializers.ReadOnlyField(source='deportista.entidad.schema_name')

    def validate(self, data):
        """
            Permite validar que no se cambie la llave a deportista en actualizacion de datos
            :param data: Datos del serializador
            :return: datos validados
            """
        if self.context['request'].method in ['PUT', 'PATCH']:
            del data['deportista']
        return data

    class Meta:
        model = HistorialLesiones
        exclude = ('fecha_creacion',)
