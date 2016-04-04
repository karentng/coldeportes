from entidades.models import Ciudad, Entidad, EscuelaDeportivaServicio
from entidades.models import *
from django.db import models
from coldeportes.utilities import calculate_age
from django.conf import settings
import os
# encoding:utf-8


class Participante(models.Model):
    ESTADO = (
        (0, 'INACTIVO'),
        (1, 'ACTIVO'),
    )
    tipo_sexo = (
        ('HOMBRE', 'MASCULINO'),
        ('MUJER', 'FEMENINO'),
    )
    TIPO_IDENTIDAD = (
        ('CC', 'CÉDULA DE CIUDADANÍA'),
        ('TI', 'TARJETA DE IDENTIDAD'),
        ('CE', 'CÉDULA DE EXTRANJERÍA'),
        ('PS', 'PASAPORTE'),
    )
    ETNIAS = (
        ('MESTIZO', 'MESTIZO'),
        ('AFROCOLOMBIANO', 'AFROCOLOMBIANO'),
        ('BLANCO', 'BLANCO'),
        ('COLOMBOINDIGENA', 'COLOMBOINDIGENA'),
        ('GITANO', 'GITANO'),
        ('PALENQUERO', 'PALENQUERO'),
        ('RAIZAL', 'RAIZAL'),
    )
    CURSO = (
        ('PRIMERO', 'PRIMERO'),
        ('SEGUNDO', 'SEGUNDO'),
        ('TERCERO', 'TERCERO'),
        ('CUARTO', 'CUARTO'),
        ('QUINTO', 'QUINTO'),
        ('SEXTO', 'SEXTO'),
        ('SEPTIMO', 'SEPTIMO'),
        ('OCTAVO', 'OCTAVO'),
        ('NOVENO', 'NOVENO'),
        ('DECIMO', 'DECIMO'),
        ('ONCE', 'ONCE'),
    )

    nombres = models.CharField(max_length=100, verbose_name='Nombres')
    apellidos = models.CharField(max_length=100, verbose_name='Apellidos')
    genero = models.CharField(choices=tipo_sexo, max_length=11, verbose_name='Genero del Participante')
    fecha_nacimiento = models.DateField(verbose_name='Fecha de nacimiento')
    tipo_id = models.CharField(max_length=10, choices=TIPO_IDENTIDAD, default='TI',
                               verbose_name='Tipo de Identificación')
    identificacion = models.CharField(max_length=100, verbose_name='Identificación')
    ciudad_residencia = models.ForeignKey(Ciudad, verbose_name='Ciudad en donde esta residiendo')
    institucion_educativa = models.CharField(max_length=255, verbose_name="Institución educativa actual")
    anho_curso = models.CharField(max_length=100, choices=CURSO, verbose_name="Año que cursa actualmente")
    telefono = models.CharField(max_length=100, verbose_name='Teléfono')
    direccion = models.CharField(max_length=100, verbose_name='Dirección')
    nacionalidad = models.ManyToManyField(Nacionalidad, verbose_name='Nacionalidad')
    eps = models.ForeignKey(EPS, verbose_name='Sistema de salud afiliado')
    entidad = models.ForeignKey(Entidad)

    etnia = models.CharField(max_length=20, choices=ETNIAS, blank=True)
    estado = models.IntegerField(default=1, choices=ESTADO)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('tipo_id', 'identificacion',)
        permissions = (
            ("view_deportista", "Permite ver deportista"),
        )

    def __str__(self):
        return self.identificacion + "-" + self.nombres+" "+self.apellidos

    def edad(self):
        return calculate_age(self.fecha_nacimiento)

    def nacionalidad_str(self):
        return ",".join(x.nombre for x in self.nacionalidad.all())

    def full_name(self):
        return str(self.nombres) + " " + str(self.apellidos)

    def full_id(self):
        return str(self.get_tipo_id_display())+":"+str(self.identificacion)

    def save(self, *args, **kwargs):
        self.nombres = self.nombres.upper()
        self.apellidos = self.apellidos.upper()
        self.direccion = self.direccion.upper()
        super(Participante, self).save(*args, **kwargs)


class EscuelaDeportiva(models.Model):

    def file_name(self, instance, filename):

        ruta = 'aval_escuelas/' + instance.nombre.strip().replace(" ", "") + filename[-4:]
        ruta_delete = settings.MEDIA_ROOT + "/" + ruta
        if os.path.exists(ruta_delete):
            os.remove(ruta_delete)
        return ruta

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

    nombre = models.CharField(max_length=100)
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
    aval = models.FileField(upload_to=file_name, null=True, blank=True,
                            verbose_name="resolución aval de funcionamiento")
    
    estado = models.IntegerField(choices=ESTADOS, default=0, verbose_name="estado de la EFD")
    # Pestañas adicionales
    servicios = models.ManyToManyField(EscuelaDeportivaServicio, blank=True)
    entidad = models.ForeignKey(Entidad)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        permissions = (
            ("view_escueladeportiva", "Permite ver escuela deportiva"),
        )

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.upper()
        self.direccion = self.direccion.upper()
        self.email = self.email.upper()
        self.barrio = self.barrio.upper()
        self.nombre_administrador = self.nombre_administrador.upper()
        super(EscuelaDeportiva, self).save(*args, **kwargs)
