#encoding:utf-8

from django.db import models
from entidades.models import Entidad
from entidades.models import Ciudad, Entidad, Nacionalidad
from coldeportes.utilities import calculate_age
#======================= ================================================================================
#Modelos para PersonalApoyo



class PersonalApoyo(models.Model):
    ESTADOS = (
        (0, "ACTIVO"),
        (1, "INACTIVO"),
        (2,'EN TRANSFERENCIA'),
        (3,'TRANSFERIDO'),
    )

    tipo_genero = (
        ('HOMBRE','HOMBRE'),
        ('MUJER','MUJER'),
        ('INDEFINIDO', 'INDEFINIDO'),
    )

    TIPO_IDENTIDAD = (
        ('TI', 'TARJETA DE IDENTIDAD'),
        ('CC', 'CÉDULA DE CIUDADANÍA'),
        ('CE', 'CÉDULA DE EXTRANJERÍA'),
        ('PS', 'PASAPORTE'),
    )

    ETNIAS = (
        ('MESTIZO','MESTIZO'),
        ('AFROCOLOMBIANO','AFROCOLOMBIANO'),
        ('BLANCO','BLANCO'),
        ('COLOMBOINDIGENA','COLOMBOINDIGENA'),
        ('GITANO','GITANO'),
        ('PALENQUERO','PALENQUERO'),
        ('RAIZAL','RAIZAL'),
    )

    ACTIVIDADES = (
        (0,'MÉDICO DEPORTÓLOGO'),
        (1,'FISIOTERAPEUTA'),
        (2,'PSICÓLOGO DEPORTIVO'),
        (3,'NUTRICIONISTA'),
        (4,'QUINESIÓLOGO'),
        (5,'QUIROPRÁCTICO'),
        (6,'PREPARADOR FÍSICO'),
        (7,'TRABAJADOR SOCIAL'),
        (8,'FISIÓLOGO'),
        (9,'BIOMECÁNICO'),
        (10,'METODÓLOGO'),
        (11,'ENTRENADOR'),
        (12,'MONITOR'),
        (13,'ENTRENADOR PERSONALIZADO'),
        (14,'ANIMADOR SOCIOCULTURAL'),
        (15,'RECREADOR'),
        (16,'PROMOTOR DE ACTIVIDAD FÍSICA'),
    )
    actividad = models.IntegerField(choices=ACTIVIDADES,verbose_name='Actividad a desempeñar')
    estado = models.IntegerField(choices=ESTADOS, default=0)
    nombres = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    genero = models.CharField(choices=tipo_genero, verbose_name='Género', max_length=11)
    foto = models.ImageField(upload_to='fotos_personal_apoyo', null=True, blank=True)
    tipo_id = models.CharField(max_length=5, verbose_name='Tipo de identificación', choices=TIPO_IDENTIDAD, default='CED')
    identificacion = models.BigIntegerField(verbose_name='Número de identificación', unique=True)
    telefono_fijo = models.CharField(max_length=50, verbose_name='Teléfono fijo', blank=True)
    telefono_celular = models.CharField(max_length=50, verbose_name='Teléfono celular', blank=True)
    correo_electronico = models.EmailField(blank=True,verbose_name='Correo electrónico')
    fecha_nacimiento = models.DateField(verbose_name='Fecha de nacimiento')
    nacionalidad = models.ManyToManyField(Nacionalidad)
    ciudad = models.ForeignKey(Ciudad, blank=True, verbose_name='Ciudad de residencia')
    etnia = models.CharField(max_length=20, choices=ETNIAS,blank=True)
    entidad = models.ForeignKey(Entidad)

    def __str__(self):
        return "%s %s"%(self.nombres, self.apellidos)

    def edad(self):
        return calculate_age(self.fecha_nacimiento)

    def nacionalidad_str(self):
        return ",".join(x.nombre for x in self.nacionalidad.all())

class FormacionDeportiva(models.Model):
    denominacion_diploma = models.CharField(max_length=150, verbose_name='Denominación del diploma')
    nivel = models.CharField(max_length=50, blank=True)
    institucion_formacion = models.CharField(max_length=100, verbose_name='Institución de formación')
    pais_formacion = models.ForeignKey(Nacionalidad)
    fecha_comienzo = models.DateField()
    actual = models.BooleanField(verbose_name='¿Aún en formación?',default=False)
    fecha_fin = models.DateField(blank=True, null=True)
    personal_apoyo = models.ForeignKey(PersonalApoyo)


class ExperienciaLaboral(models.Model):
    nombre_cargo = models.CharField(max_length=50, verbose_name='Nombre del cargo')
    institucion = models.CharField(max_length=150, verbose_name='Institución donde se desempeñó')
    fecha_comienzo = models.DateField()
    actual = models.BooleanField(verbose_name='¿Aún en el cargo?',default=False)
    fecha_fin = models.DateField(blank=True, null=True)
    personal_apoyo = models.ForeignKey(PersonalApoyo)