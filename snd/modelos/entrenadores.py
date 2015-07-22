#encoding:utf-8

from django.db import models
from entidades.models import Ciudad, Entidad, Nacionalidad, TipoDisciplinaDeportiva
#=======================================================================================================
#Modelos para Entrenadores

class Entrenador(models.Model):
    ESTADOS = (
        (0, "ACTIVO"),
        (1, "INACTIVO"),
        (2,'EN TRANSFERENCIA'),
        (3,'TRANSFERIDO'),
    )

    tipo_genero = (
        ('HOMBRE','HOMBRE'),
        ('MUJER','MUJER'),
        ('LGTBI', 'LGTBI'),
    )

    TIPO_IDENTIDAD = (
        ('CED', 'CÉDULA DE CIUDADANÍA'),
        ('CEDEX', 'CÉDULA DE EXTRANJERO'),
        ('PAS', 'PASAPORTE'),
    )

    ETNIAS = (
        ('MESTIZO','MESTIZO'),
        ('AFROCOLOMBIANO','AFROCOLOMBIANO'),
        ('BLANCOS','BLANCOS'),
        ('COLOMBOINDIGENA','COLOMBOINDIGENA'),
        ('GITANO','GITANO'),
    )
    estado = models.IntegerField(choices=ESTADOS, default=0)
    nombres = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    genero = models.CharField(choices=tipo_genero, verbose_name='Género', max_length=11)
    foto = models.ImageField(upload_to='fotos_entrenadores', null=True, blank=True)
    tipo_id = models.CharField(max_length=5, verbose_name='Tipo de identificación', choices=TIPO_IDENTIDAD, default='CED')
    identificacion = models.BigIntegerField(verbose_name='Número de identificación', unique=True)
    telefono_fijo = models.CharField(max_length=50, verbose_name='Teléfono fijo', blank=True)
    telefono_celular = models.CharField(max_length=50, verbose_name='Teléfono celular', blank=True)
    correo_electronico = models.EmailField(blank=True,verbose_name='Correo electrónico')
    fecha_nacimiento = models.DateField(verbose_name='Fecha de nacimiento')
    nacionalidad = models.ManyToManyField(Nacionalidad)
    ciudad = models.ForeignKey(Ciudad, blank=True)
    #en centimetros
    altura = models.IntegerField(blank=True, null=True, verbose_name='Altura (En Cm)')
    #en Kg
    peso = models.IntegerField(blank=True, null=True, verbose_name='Peso (En Kg)')
    etnia = models.CharField(max_length=20, choices=ETNIAS,blank=True)
    entidad_vinculacion = models.ForeignKey(Entidad)

class FormacionDeportiva(models.Model):
    disciplina_deportiva = models.ManyToManyField(TipoDisciplinaDeportiva)
    denominacion_diploma = models.CharField(max_length=150, verbose_name='Denominación del diploma')
    nivel = models.CharField(max_length=50, blank=True)
    institucion_formacion = models.CharField(max_length=100, verbose_name='Institución de formación')
    pais_formacion = models.ForeignKey(Nacionalidad)
    fecha_comienzo = models.DateField()
    actual = models.BooleanField(verbose_name='¿Aún en formación?',default=False)
    fecha_fin = models.DateField(blank=True, null=True)
    entrenador = models.ForeignKey(Entrenador)


class ExperienciaLaboral(models.Model):
    nombre_cargo = models.CharField(max_length=50, verbose_name='Nombre del cargo')
    institucion = models.CharField(max_length=150, verbose_name='Institución donde se desempeñó')
    fecha_comienzo = models.DateField()
    actual = models.BooleanField(verbose_name='¿Aún en el cargo?',default=False)
    fecha_fin = models.DateField(blank=True, null=True)
    entrenador = models.ForeignKey(Entrenador)