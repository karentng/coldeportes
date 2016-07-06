from django.db import models
from snd.models import Deportista,ComposicionCorporal,HistorialDeportivo,InformacionAcademica,InformacionAdicional,HistorialLesiones
from rest_framework import serializers

# Create your models here.
class DeportistaSerializable(serializers.ModelSerializer):
    entidad = serializers.ReadOnlyField(source='entidad.schema_name')

    class Meta:
        model = Deportista
        exclude = ('fecha_creacion',)

class ComposicionCorporalSerializable(serializers.ModelSerializer):
    entidad = serializers.ReadOnlyField(source='deportista.entidad.schema_name')

    class Meta:
        model = ComposicionCorporal
        exclude = ('fecha_creacion',)

class HistorialDeportivoSerializable(serializers.ModelSerializer):
    entidad = serializers.ReadOnlyField(source='deportista.entidad.schema_name')

    class Meta:
        model = HistorialDeportivo
        exclude = ('fecha_creacion',)

class InformacionAcademicaSerializable(serializers.ModelSerializer):
    entidad = serializers.ReadOnlyField(source='deportista.entidad.schema_name')

    class Meta:
        model = InformacionAcademica
        exclude = ('fecha_creacion',)

class InformacionAdicionalSerializable(serializers.ModelSerializer):
    entidad = serializers.ReadOnlyField(source='deportista.entidad.schema_name')

    class Meta:
        model = InformacionAdicional
        exclude = ('fecha_creacion',)

class HistorialLesionesSerializable(serializers.ModelSerializer):
    entidad = serializers.ReadOnlyField(source='deportista.entidad.schema_name')

    class Meta:
        model = HistorialLesiones
        exclude = ('fecha_creacion',)
