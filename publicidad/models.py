from django.db import models
from datetime import datetime, timedelta

# Create your models here.
class Clasificado(models.Model):
    CATEGORIAS =(
        (0,'Empleo'),
        (1,'Compra/Venta'),
        (2,'Otros'),
    )


    foto = models.ImageField(upload_to='fotos_noticias')
    categoria = models.IntegerField(choices=CATEGORIAS)
    titulo = models.CharField(max_length=150)
    descripcion = models.TextField()
    contacto = models.CharField(max_length=150)
    fecha_publicacion = models.DateField(auto_now_add=True)
    fecha_expiracion = models.DateField()
    valor = models.PositiveIntegerField(null=True, blank=True)
    etiquetas = models.CharField(max_length=255,null=True,blank=True)
    estado = models.IntegerField(default=1)

    class Meta:
        permissions = (
            ("view_noticia", "Permite ver noticia"),
        )