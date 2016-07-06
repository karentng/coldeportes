from django.db import models
from snd.models import Deportista,ComposicionCorporal,HistorialDeportivo,InformacionAcademica,InformacionAdicional,HistorialLesiones
from rest_framework import serializers

# Create your models here.
class DeportistaSerializable(serializers.ModelSerializer):
    entidad = serializers.ReadOnlyField(source='entidad.nombre')

    class Meta:
        model = Deportista
        exclude = ('fecha_creacion',)

class ComposicionCorporalSerializable(serializers.ModelSerializer):
    deportista = serializers.ReadOnlyField(source='deportista.identificacion')

    class Meta:
        model = ComposicionCorporal
        exclude = ('fecha_creacion',)

class HistorialDeportivoSerializable(serializers.ModelSerializer):
    deportista = serializers.ReadOnlyField(source='deportista.identificacion')

    class Meta:
        model = HistorialDeportivo
        exclude = ('fecha_creacion',)

class InformacionAcademicaSerializable(serializers.ModelSerializer):
    deportista = serializers.ReadOnlyField(source='deportista.identificacion')

    class Meta:
        model = InformacionAcademica
        exclude = ('fecha_creacion',)

class InformacionAdicionalSerializable(serializers.ModelSerializer):
    deportista = serializers.ReadOnlyField(source='deportista.identificacion')

    class Meta:
        model = InformacionAdicional
        exclude = ('fecha_creacion',)

class HistorialLesionesSerializable(serializers.ModelSerializer):
    deportista = serializers.ReadOnlyField(source='deportista.identificacion')

    class Meta:
        model = HistorialLesiones
        exclude = ('fecha_creacion',)
