from django.db import models


# Create your models here.
class Clasificado(models.Model):
    CATEGORIAS = (
        (0, 'Empleo'),
        (1, 'Compra/Venta'),
        (2, 'Otros'),
    )

    foto = models.ImageField(upload_to='fotos_noticias')
    categoria = models.IntegerField(choices=CATEGORIAS, verbose_name="Categoría del clasificado")
    titulo = models.CharField(max_length=40, verbose_name="Título")
    descripcion = models.TextField(max_length=800, verbose_name="Descripción")
    contacto = models.CharField(max_length=150, verbose_name="Información de contacto")
    fecha_publicacion = models.DateField(verbose_name="Fecha de publicación")
    fecha_expiracion = models.DateField(verbose_name="Fecha de finalización")
    valor = models.PositiveIntegerField(null=True, blank=True)
    etiquetas = models.CharField(max_length=255, null=True, blank=True)
    estado = models.IntegerField(default=1)
    archivo_adjunto = models.FileField(upload_to="clasificados/archivos_adjuntos/", blank=True, null=True,
                                       verbose_name="Archivo adjunto (opcional)")

    def get_estado_accion(self):
        return ("inactivado", "activado")[int(self.estado)]

    class Meta:
        permissions = (
                ("view_clasificado", "Permite ver clasificados"),
            )
