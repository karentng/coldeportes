from django.db import models


# Create your models here.
class Noticia(models.Model):

    foto = models.ImageField(upload_to='fotos_noticias')
    titulo = models.CharField(max_length=40, verbose_name="Título de la noticia")
    fecha_inicio = models.DateField(verbose_name="Fecha de inicio")
    fecha_expiracion = models.DateField(verbose_name="Fecha de finalización")
    autor = models.CharField(max_length=40)
    cuerpo_noticia = models.TextField(verbose_name="Cuerpo de la noticia")
    etiquetas = models.CharField(max_length=255, null=True, blank=True)
    estado = models.IntegerField(default=1)
