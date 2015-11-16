from entidades.models import *
from django.db import models

class CentroBiomedico(models.Model):
    ESTADOS = (
        (0, "ACTIVO"),
        (1, "INACTIVO"),
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
    telefono_fijo = models.CharField(max_length=50, verbose_name='Teléfono fijo')
    email = models.EmailField(null=True,blank=True)
    web = models.URLField(verbose_name="página web", blank=True, null=True)
    nombre_administrador = models.CharField(max_length=50, blank=True, null=True)
    telefono_celular = models.CharField(max_length=50, verbose_name='Teléfono celular', blank=True)
    ciudad = models.ForeignKey(Ciudad)
    comuna = models.PositiveIntegerField()
    barrio = models.CharField(max_length=20)
    estrato = models.IntegerField(choices=ESTRATOS)
    
    estado = models.IntegerField(choices=ESTADOS, default=0, verbose_name="estado del Centro Biomédico")
    # Pestañas adicionales
    servicios = models.ManyToManyField(CentroBiomedicoServicio, blank=True)
    entidad = models.ForeignKey(Entidad)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        permissions = (
            ("view_centrobiomedico", "Permite ver centro biomedico"),
        )

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.upper()
        self.direccion = self.direccion.upper()
        self.email = self.email.upper()
        self.barrio = self.barrio.upper()
        self.nombre_administrador = self.nombre_administrador.upper()
        super(CentroBiomedico, self).save(*args, **kwargs)

    def obtenerAtributos(self):
        atributos = [
            ["Nombre", self.nombre],
            ["Teléfono", self.telefono_fijo],
            ["Correo electrónico", self.email],
            ["Página Web", self.web],
            ["Ciudad", self.ciudad],
            ["Dirección", self.direccion],
            ["Barrio", self.barrio],
            ["Comuna", self.comuna],
            ["Estrato", self.estrato],
            ["Administrador", self.nombre_administrador],
            ["Teléfono Administrador", self.telefono_celular],
        ]

        return [None, atributos, None, None, "Centros Biomédicos!"]
