from django.db import models

# Create your models here.
class Articulo(models.Model):

    ACTORES = (
        ('CF', 'CAF'),
        ('CC', 'Caja de Compensación'),
        ('DE', 'Deportista'),
        ('DI', 'Dirigente'),
        ('ES', 'Escenario'),
        ('EC', 'Escuela'),
        ('PA', 'Personal de Apoyo'),
    )

    titulo =  models.CharField(max_length=100,unique=True, verbose_name="título del artículo")
    subtitulo = models.CharField(max_length=100, verbose_name="subtítulo del artículo")
    palabras_clave = models.CharField(max_length=1024, verbose_name='palabras clave')
    imagen = models.FileField( verbose_name="imagen", null=True, blank=True)
    contenido = models.TextField()
    actor = models.CharField(choices=ACTORES, max_length=2)
