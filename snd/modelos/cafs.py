#encoding:utf-8
from django.db import models
from entidades.models import Ciudad, Entidad, CAClase, CAServicio

class CentroAcondicionamiento(models.Model):
    ESTADOS = (
        (0, "Activo"),
        (1, "Inactivo"),
    )
    
    ESTRATOS = (
        (1, 'Uno'),
        (2, 'Dos'),
        (3, 'Tres'),
        (4, 'Cuatro'),
        (5, 'Cinco'),
        (6, 'Seis'),
    )
    nombre =  models.CharField(max_length=100)
    direccion = models.CharField(max_length=100, verbose_name="dirección")
    telefono = models.CharField(max_length=50, verbose_name="teléfono")
    email = models.EmailField()
    web = models.URLField(verbose_name="página web", blank=True, null=True)
    nombre_administrador = models.CharField(max_length=50, blank=True, null=True)
    ciudad = models.ForeignKey(Ciudad)
    comuna = models.PositiveIntegerField()
    barrio = models.CharField(max_length=20)
    estrato = models.IntegerField(choices=ESTRATOS)
    latitud = models.FloatField(null=True, blank=True)
    longitud = models.FloatField(null=True, blank=True)
    altura = models.PositiveIntegerField(null=True, blank=True)
    
    estado = models.IntegerField(choices=ESTADOS, default=0, verbose_name="estado del Centro de Acondicionamiento Físico")
    # Pestañas adicionales
    servicios = models.ManyToManyField(CAServicio, blank=True)
    clases = models.ManyToManyField(CAClase, blank=True)
    entidad = models.ForeignKey(Entidad)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        permissions = (
                ("view_centroacondicionamiento", "Permite ver centro acondicionamiento"),
            )

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.upper()
        self.direccion = self.direccion.upper()
        self.email = self.email.upper()
        self.barrio = self.barrio.upper()
        self.nombre_administrador = self.nombre_administrador.upper()
        super(CentroAcondicionamiento, self).save(*args, **kwargs)

    def obtenerAtributos(self):
        from django.conf import settings
        imagen = None
        fotos = CAFoto.objects.filter(centro=self)
        if len(fotos) > 0:
            imagen = ("%s%s")%(settings.MEDIA_URL, fotos[0].foto.__str__())
        else:
            imagen = ("%s%s")%(settings.STATIC_URL, "img/actores/CAFView.PNG")

        atributos = [
            ["Nombre", self.nombre],
            ["Ciudad", self.ciudad.nombre],
            ["Comuna", self.comuna],
            ["Barrio", self.barrio],
            ["Estrato", self.estrato],
            ["Dirección", self.direccion],
            ["Teléfono", self.telefono],
            ["Latitud", self.latitud],
            ["Longitud", self.longitud],
        ]

        return [imagen, atributos, self.latitud, self.longitud, "CAF!"]

class CAPlan(models.Model):
    centro = models.ForeignKey(CentroAcondicionamiento)
    nombre = models.CharField(max_length=255)
    precio = models.PositiveIntegerField()
    descripcion = models.TextField(verbose_name="descripción")
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.upper()
        self.descripcion = self.descripcion.upper()
        super(CAPlan, self).save(*args, **kwargs)

def ruta_fotos_cafs(instance, filename):
    return "snd/fotos/cafs/%s-%s"%(instance.id, filename.encode('ascii','ignore').decode('ascii'))

class CAFoto(models.Model):
    centro = models.ForeignKey(CentroAcondicionamiento)
    titulo = models.CharField(max_length=255, verbose_name="título")
    foto = models.ImageField(upload_to=ruta_fotos_cafs)
    descripcion = models.TextField(blank=True, null=True, verbose_name="descripción")
    fecha_creacion = models.DateTimeField(auto_now_add=True)