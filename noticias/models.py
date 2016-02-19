from django.db import models
from ckeditor.fields import RichTextField


# Create your models here.
class Noticia(models.Model):

    foto = models.ImageField(upload_to='fotos_noticias')
    titulo = models.CharField(max_length=40)
    fecha_publicacion = models.DateField(auto_now_add=True)
    fecha_expiracion = models.DateField()
    autor = models.CharField(max_length=40)
    cuerpo_noticia = RichTextField(config_name='default', verbose_name=" ")
    etiquetas = models.CharField(max_length=255,null=True, blank=True)
    estado = models.IntegerField(default=1)
