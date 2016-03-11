from django.db import models
from noticias.models import Noticia


# Create your models here.
class Participante(models.Model):
    TIPO_IDENTIDAD = (
        ('CC', 'CÉDULA DE CIUDADANÍA'),
        ('TI', 'TARJETA DE IDENTIDAD'),
        ('CE', 'CÉDULA DE EXTRANJERÍA'),
        ('PS', 'PASAPORTE'),
    )

    evento_participe = models.IntegerField()
    tipo_id = models.CharField(max_length=10, choices=TIPO_IDENTIDAD, default='CC',
                               verbose_name='Tipo de Identificación')
    identificacion = models.CharField(max_length=100, verbose_name='Identificación')
    nombre = models.CharField(max_length=155)
    apellido = models.CharField(max_length=155)
    fecha_nacimiento = models.DateField(verbose_name='Fecha de nacimiento')
    email = models.EmailField()

    class Meta:
        unique_together = ('evento_participe', 'identificacion')


class Evento(models.Model):

    titulo_evento = models.CharField(max_length=255, verbose_name="Título del evento")
    lugar_evento = models.CharField(max_length=255, verbose_name="Lugar de realización del evento")
    fecha_inicio = models.DateField(verbose_name="Fecha de inicio del evento")
    fecha_finalizacion = models.DateField(verbose_name="Fecha de finalización del evento")
    fecha_inicio_preinscripcion = models.DateField(verbose_name="Fecha de inicio de las preinscripciones")
    fecha_finalizacion_preinscripcion = models.DateField(verbose_name="Fecha de finalización de las preinscripciones")
    imagen = models.ImageField()
    video = models.CharField(max_length=255, verbose_name="Vídeo del evento", blank=True, null=True)
    descripcion_evento = models.TextField(verbose_name="Descripción del evento (se usará como cuerpo de noticia)")
    costo_entrada = models.PositiveIntegerField(verbose_name="Costo de la entrada", blank=True, null=True)
    cupo_participantes = models.PositiveIntegerField(verbose_name="Cupo para participantes")
    cupo_disponible = models.PositiveIntegerField()
    noticia = models.ForeignKey(Noticia)
    participantes = models.ManyToManyField(Participante)
    autor = models.CharField(verbose_name="Autor de la noticia", max_length=150,
                             help_text="Se usará como autor para la noticia del evento que se creará")
    estado = models.IntegerField(default=1)
