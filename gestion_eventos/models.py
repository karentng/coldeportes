from django.db import models
from noticias.models import Noticia

# Create your models here.
class Evento(models.Model):

    titulo_evento = models.CharField(max_length=255, verbose_name="Título del evento")
    lugar_evento = models.CharField(max_length=255, verbose_name="Lugar de realización del evento")
    fecha_inicio = models.DateField(verbose_name="Fecha de inicio del evento")
    fecha_finalizacion = models.DateField(verbose_name="Fecha de finalización del evento")
    fecha_inicio_preinscripcion = models.DateField(verbose_name="Fecha de inicio de las preinscripciones")
    fecha_finalizacion_preinscripcion = models.DateField(verbose_name="Fecha de finalización de las preinscripciones")
    imagen = models.ImageField()
    video = models.CharField(max_length=255, verbose_name="Vídeo del evento", blank=True, null=True)
    descripcion_evento = models.TextField(verbose_name="Descripción del evento (se usara como cuerpo de noticia)")
    costo_entrada = models.PositiveIntegerField(verbose_name="Costo de la entrada", blank=True, null=True)
    cupo_participantes = models.PositiveIntegerField(verbose_name="Cupo para participantes")
    noticia = models.ForeignKey(Noticia)
    participantes = models.ManyToManyField(Participante)
    autor = models.CharField(verbose_name="Autor de la noticia", max_length=150)
    estado = models.IntegerField(default=1)


class Participante(models.Model):

    cedula = models.CharField(max_length=20)
