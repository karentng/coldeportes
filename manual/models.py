from django.db import models
from ckeditor.fields import RichTextField
# Create your models here.
class Articulo(models.Model):

    MODULOS = (
        ('CF', 'CAFs'),
        ('CC', 'Caja de Compensaciones'),
        ('DE', 'Deportistas'),
        ('DR', 'Directorio'),
        ('DI', 'Dirigentes'),
        ('ES', 'Escenarios'),
        ('EC', 'Escuelas'),
        ('NO', 'Normograma'),
        ('NT', 'Noticias'),
        ('PA', 'Personal de Apoyo'),
        ('TR', 'Transferencias'),
    )

    USUARIOS = (
        ('AD', 'Administrador'),
        ('DI', 'Digitador'),
        ('SL', 'Solo Lectura'),
    )

    titulo =  models.CharField(max_length=100,unique=True, verbose_name="título del artículo")
    orden = models.FloatField()
    subtitulo = models.CharField(max_length=100, verbose_name="subtítulo del artículo")
    palabras_clave = models.CharField(max_length=1024, verbose_name='palabras clave')
    modulo = models.CharField(choices=MODULOS, max_length=2)
    usuario = models.CharField(choices=USUARIOS, max_length=2)
    contenido = RichTextField(config_name='default', verbose_name=" ")
