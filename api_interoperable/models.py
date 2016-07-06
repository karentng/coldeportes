from django.db import models
from snd.models import Deportista,ComposicionCorporal,HistorialDeportivo,InformacionAcademica,InformacionAdicional,HistorialLesiones
from rest_framework import serializers

# Create your models here.
class DeportistaSerializable(serializers.ModelSerializer):
    class Meta:
        model = Deportista
        exclude = ('fecha_creacion',)

class DeportistaPublicSerializable(serializers.ModelSerializer):
    class Meta:
        model = Deportista
        exclude = ('tipo_id','identificacion','barrio','comuna','email','telefono','direccion','lgtbi','etnia','fecha_creacion',)

class ComposicionCorporalSerializable(serializers.ModelSerializer):
    class Meta:
        model = ComposicionCorporal
        exclude = ('fecha_creacion',)

class HistorialDeportivoSerializable(serializers.ModelSerializer):
    class Meta:
        model = HistorialDeportivo
        exclude = ('fecha_creacion',)

class InformacionAcademicaSerializable(serializers.ModelSerializer):
    class Meta:
        model = InformacionAcademica
        exclude = ('fecha_creacion',)

class InformacionAdicionalSerializable(serializers.ModelSerializer):
    class Meta:
        model = InformacionAdicional
        exclude = ('fecha_creacion',)

class HistorialLesionesSerializable(serializers.ModelSerializer):
    class Meta:
        model = HistorialLesiones
        exclude = ('fecha_creacion',)