#encoding:utf-8

from entidades.models import *
from django.db import models
from django.conf import settings
import os

class Dirigente(models.Model):
    def foto_name(instance, filename):
        #el nombre de la imagen es la identificación del dirigente, filename[-4:] indica la extensión del archivo
        #primero se borra alguna imagen existente que tenga el mismo nombre. Si la imagen anterior tiene una extensión distinta a la nueva se crea una copia
        ruta = 'fotos_dirigentes/' + instance.identificacion + filename[-4:]
        ruta_delete = settings.MEDIA_ROOT + "/" + ruta
        if(os.path.exists(ruta_delete)):
            os.remove(ruta_delete)
        return ruta

    TIPO_GENERO = (
        ('HOMBRE','HOMBRE'),
        ('MUJER','MUJER'),
    )
    TIPO_IDENTIFICACION = (
        ('CC', 'CÉDULA DE CIUDADANÍA'),
        ('CE', 'CÉDULA DE EXTRANJERÍA'),
        ('PS', 'PASAPORTE'),
    )
    ESTADOS = (
        (0, "ACTIVO"),
        (1, "INACTIVO"),
    )

    tipo_identificacion = models.CharField(choices=TIPO_IDENTIFICACION, max_length=2, verbose_name="Tipo de identificación")
    identificacion = models.CharField(max_length=20, verbose_name="Número de identificación", unique=True)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    genero = models.CharField(choices=TIPO_GENERO,max_length=6, verbose_name='Género')
    nacionalidad = models.ManyToManyField(Nacionalidad)
    telefono_fijo = models.CharField(max_length=50, verbose_name='Teléfono fijo')
    telefono_celular = models.CharField(max_length=50, verbose_name='Teléfono celular', blank=True)
    email = models.EmailField(null=True,blank=True)
    ciudad_residencia = models.ForeignKey(Ciudad, verbose_name="Ciudad de residencia")
    foto = models.ImageField(upload_to=foto_name, null=True, blank=True)
    perfil = models.TextField(max_length=500, verbose_name="Perfil profesional")

    entidad = models.ForeignKey(Entidad, null=True, blank=True)
    estado = models.IntegerField(choices=ESTADOS, default=0, verbose_name="Estado del dirigente")

    def __str__(self):
        return "{0} {1}".format(self.nombres, self.apellidos)

    def save(self, *args, **kwargs):
        self.nombres = self.nombres.upper()
        self.apellidos = self.apellidos.upper()
        super(Dirigente, self).save(*args, **kwargs)

class DirigenteCargo(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre del cargo")
    fecha_posesion = models.DateField(verbose_name="Fecha de posesión")
    fecha_retiro = models.DateField(null=True,blank=True, verbose_name="Fecha de retiro")
    superior = models.ForeignKey(Dirigente, null=True, blank=True, related_name='superior')
    superior_cargo = models.ForeignKey('self', null=True, blank=True, verbose_name="Cargo del superior")
    dirigente = models.ForeignKey(Dirigente, related_name='dirigente')

    def __str__(self):
        if self.fecha_retiro != None:
            fecha_retiro = self.get_fecha_format(self.fecha_retiro)
        else:
            fecha_retiro = 'Actual'
        return "{0} [{1} a {2}]".format(self.nombre, self.get_fecha_format(self.fecha_posesion), fecha_retiro)

    def periodo(self):
        if self.fecha_retiro != None:
            fecha_retiro = self.get_fecha_format(self.fecha_retiro)
        else:
            fecha_retiro = 'Actual'
        return "{0} a {1}".format(self.get_fecha_format(self.fecha_posesion), fecha_retiro)

    def get_fecha_format(self,fecha):
        meses = ["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
        return str(fecha.day) + " de " + meses[fecha.month-1] + " de " + str(fecha.year)

class DirigenteFuncion(models.Model):
    dirigente = models.ForeignKey(Dirigente)
    cargo = models.ForeignKey(DirigenteCargo)
    descripcion = models.TextField(max_length=500, verbose_name="Función")


