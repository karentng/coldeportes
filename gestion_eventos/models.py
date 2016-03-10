from django.db import models


# Create your models here.
class Evento(models.Model):

    titulo_evento = models.CharField()
    fecha_inicio = models.DateField()
    fecha_finalizacion = models.DateField()
    fecha_inicio_preinscripcion = models.DateField()
    fecha_finalizacion_preinscripcion = models.DateField()
    imagen = models.ImageField()
    video = models.CharField()
    descripcion_evento = models.TextField()
    costo_entrada = models.CharField()
    cupo_participantes = models.PositiveIntegerField()