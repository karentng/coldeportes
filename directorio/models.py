from django.db import models
from entidades.models import *
from snd.models import *


# Create your models here.
class EscenarioView(models.Model):
    class Meta:
        managed = False
    #campos modelo escenario
    nombre =  models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
    latitud = models.FloatField(max_length=10)
    longitud = models.FloatField(max_length=10)
    altura = models.FloatField(max_length=10)
    ciudad = models.ForeignKey(Ciudad)
    comuna = models.CharField(max_length=10)
    barrio = models.CharField(max_length=20)
    estrato = models.CharField(max_length=1)
    nombre_administrador = models.CharField(max_length=50, null=True)
    entidad = models.ForeignKey(Entidad)    
    estado = models.IntegerField()
    #campos modelo contacto
    nombre_contacto =  models.CharField(max_length=50)
    telefono_contacto = models.CharField(max_length=20)
    email_contacto = models.EmailField()
    descripcion_contacto = models.CharField(max_length=1024, null=True)
    #campos modelo horario
    horario_id = models.IntegerField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    dias = models.ForeignKey(Dias)
    descripcion_horario = models.CharField(max_length=1024)
    #campos modelo Foto
    foto = models.ImageField(upload_to='fotos_escenarios', null=True, blank=True)
    #campo pra búsqueda
    contenido = models.TextField()

class CAFView(models.Model):
    class Meta:
        managed = False
    #campos cafs
    nombre =  models.CharField(max_length=100)
    direccion = models.CharField(max_length=100, verbose_name="dirección")
    latitud = models.FloatField(max_length=10)
    longitud = models.FloatField(max_length=10)
    telefono = models.CharField(max_length=50, verbose_name="teléfono")
    altura = models.FloatField(max_length=10)    
    email = models.EmailField()
    web = models.URLField(verbose_name="página web", blank=True, null=True)
    ciudad = models.ForeignKey(Ciudad)
    comuna = models.CharField(max_length=10)
    barrio = models.CharField(max_length=20)
    estrato = models.IntegerField()
    nombre_administrador = models.CharField(max_length=50, blank=True, null=True)
    entidad = models.ForeignKey(Entidad)
    estado = models.IntegerField()
    #campo de modelo CAfoto
    foto = models.ImageField(upload_to='ruta_fotos_cafs')
    #campo pra búsqueda
    contenido = models.TextField()

