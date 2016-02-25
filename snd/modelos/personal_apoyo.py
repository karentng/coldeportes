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
        ('HOMBRE','MASCULINO'),
        ('MUJER','FEMENINO'),
    )

    TIPO_IDENTIDAD = (
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
        (14,'ANIMADOR SOCIOCULTURAL'),
        (9,'BIOMECÁNICO'),
        (11,'ENTRENADOR'),
        (13,'ENTRENADOR PERSONALIZADO'),
        (8,'FISIÓLOGO'),
        (1,'FISIOTERAPEUTA'),
        (0,'MÉDICO DEPORTÓLOGO'),
        (10,'METODÓLOGO'),
        (12,'MONITOR'),
        (3,'NUTRICIONISTA'),
        (6,'PREPARADOR FÍSICO'),
        (16,'PROMOTOR DE ACTIVIDAD FÍSICA'),
        (2,'PSICÓLOGO DEPORTIVO'),
        (4,'QUINESIÓLOGO'),
        (5,'QUIROPRÁCTICO'),
        (15,'RECREADOR'),
        (7,'TRABAJADOR SOCIAL'),
    )

    actividad = models.IntegerField(choices=ACTIVIDADES,verbose_name='Actividad a desempeñar')
    estado = models.IntegerField(choices=ESTADOS, default=0)
    nombres = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    genero = models.CharField(choices=tipo_genero, verbose_name='Género', max_length=11)
    foto = models.ImageField(upload_to='fotos_personal_apoyo', null=True, blank=True)
    tipo_id = models.CharField(max_length=5, verbose_name='Tipo de identificación', choices=TIPO_IDENTIDAD)
    identificacion = models.CharField(max_length=100,verbose_name='Número de identificación', unique=True)
    telefono_fijo = models.CharField(max_length=50, verbose_name='Teléfono fijo', blank=True)
    telefono_celular = models.CharField(max_length=50, verbose_name='Teléfono celular', blank=True)
    correo_electronico = models.EmailField(blank=True,verbose_name='Correo electrónico')
    fecha_nacimiento = models.DateField(verbose_name='Fecha de nacimiento')
    nacionalidad = models.ManyToManyField(Nacionalidad)
    ciudad = models.ForeignKey(Ciudad, verbose_name='Ciudad de residencia')
    etnia = models.CharField(max_length=20, choices=ETNIAS,blank=True)
    lgtbi = models.BooleanField(verbose_name='Hace parte de la comunidad LGTBI?')
    entidad = models.ForeignKey(Entidad)
    fecha_creacion = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('tipo_id','identificacion',)
        permissions = (
            ("view_personalapoyo", "Permite ver personal apoyo"),
        )

    def __str__(self):
        return "%s - %s %s"%(self.identificacion,self.nombres, self.apellidos)

    def edad(self):
        return calculate_age(self.fecha_nacimiento)

    def nacionalidad_str(self):
        return ",".join(x.nombre for x in self.nacionalidad.all())

    def fotos(self):
        return [self.foto]


class FormacionDeportiva(models.Model):
    tipo_academica = (
        ('Técnico','Técnico'),
        ('Tecnólogo','Tecnólogo'),
        ('Pregrado','Pregrado'),
        ('Postgrado','Postgrado'),
    )
    tipo_estado = (
        ('Actual','Actual'),
        ('Finalizado','Finalizado'),
        ('Incompleto','Incompleto'),
    )
    pais = models.ForeignKey(Nacionalidad,verbose_name='País')
    institucion = models.CharField(max_length=100,verbose_name='Institución')
    nivel = models.CharField(choices=tipo_academica,max_length=20,verbose_name='Nivel')
    estado = models.CharField(choices=tipo_estado,max_length=20,verbose_name='Estado')
    profesion =  models.CharField(max_length=100,blank=True,null=True,verbose_name='Profesión')
    grado_semestre = models.IntegerField(verbose_name='Grado, año o semestre', null=True, blank=True)
    fecha_finalizacion = models.IntegerField(blank=True,null=True,verbose_name='Año finalización')
    fecha_creacion = models.DateField(auto_now_add=True)
    personal_apoyo = models.ForeignKey(PersonalApoyo)

    def save(self, *args, **kwargs):
        self.institucion = self.institucion.upper()
        self.profesion = self.profesion.upper()
        super(FormacionDeportiva, self).save(*args, **kwargs)


class ExperienciaLaboral(models.Model):
    nombre_cargo = models.CharField(max_length=50, verbose_name='Nombre del cargo')
    institucion = models.CharField(max_length=150, verbose_name='Institución donde se desempeñó')
    fecha_comienzo = models.DateField()
    actual = models.BooleanField(verbose_name='¿Aún en el cargo?',default=False)
    fecha_fin = models.DateField(blank=True, null=True)
    fecha_creacion = models.DateField(auto_now_add=True)
    personal_apoyo = models.ForeignKey(PersonalApoyo)