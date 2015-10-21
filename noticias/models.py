from django.db import models

# Create your models here.
class Noticia(models.Model):
    titulo = models.CharField(max_length=150)
    cuerpo_noticia = models.TextField()
    foto = models.ImageField(upload_to='fotos_noticias')
    fecha_publicacion = models.DateField(auto_now_add=True)