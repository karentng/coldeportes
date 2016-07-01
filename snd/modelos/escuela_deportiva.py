from entidades.models import Ciudad, Entidad, EscuelaDeportivaServicio
from entidades.models import *
from django.db import models
from coldeportes.utilities import calculate_age
from django.conf import settings
import os
# encoding:utf-8

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


class EscuelaDeportiva(models.Model):

    def file_name(self, instance, filename):

        ruta = 'aval_escuelas/' + instance.nombre.strip().replace(" ", "") + filename[-4:]
        ruta_delete = settings.MEDIA_ROOT + "/" + ruta
        if os.path.exists(ruta_delete):
            os.remove(ruta_delete)
        return ruta

    ESTRATOS = (
        (1, 'Uno'),
        (2, 'Dos'),
        (3, 'Tres'),
        (4, 'Cuatro'),
        (5, 'Cinco'),
        (6, 'Seis'),
    )
    TIPO_SEDE = (
        ("PRINCIPAL", "PRINCIPAL"),
        ("SECUNDARIA", "SECUNDARIA"),
    )

    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100, verbose_name="Dirección")
    telefono_fijo = models.CharField(max_length=50, verbose_name='Teléfono fijo')
    email = models.EmailField(null=True, blank=True)
    web = models.URLField(verbose_name="página web", blank=True, null=True)
    nombre_administrador = models.CharField(max_length=50, blank=True, null=True)
    telefono_celular = models.CharField(max_length=50, verbose_name='Teléfono celular', blank=True)
    tipo_sede = models.CharField(max_length=150, choices=TIPO_SEDE, verbose_name="Tipo de sede")
    ciudad = models.ForeignKey(Ciudad)
    comuna = models.PositiveIntegerField()
    barrio = models.CharField(max_length=20)
    estrato = models.IntegerField(choices=ESTRATOS)
    aval = models.FileField(upload_to=file_name, null=True, blank=True,
                            verbose_name="resolución aval de funcionamiento")
    descripcion_lugar = models.TextField(verbose_name="Descripción del lugar", max_length=500)
    estado = models.IntegerField(choices=ESTADO, default=0, verbose_name="estado de la EFD")
    # Pestañas adicionales
    servicios = models.ManyToManyField(EscuelaDeportivaServicio, blank=True)
    entidad = models.ForeignKey(Entidad)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        permissions = (
            ("view_escueladeportiva", "Permite ver escuela deportiva"),
        )

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.upper()
        self.direccion = self.direccion.upper()
        self.email = self.email.upper()
        self.barrio = self.barrio.upper()
        self.nombre_administrador = self.nombre_administrador.upper()
        super(EscuelaDeportiva, self).save(*args, **kwargs)


class CategoriaEscuela(models.Model):
    sede = models.ForeignKey(EscuelaDeportiva)
    nombre_categoria = models.CharField(max_length=155, verbose_name="Nombre Categoría")
    edad_minima = models.PositiveIntegerField(verbose_name="Edad Mínima")
    edad_maxima = models.PositiveIntegerField(verbose_name="Edad Máxima")
    descripcion = models.TextField(max_length=500, verbose_name="Descripción", null=True, blank=True)

    def __str__(self):
        return self.nombre_categoria + " -- " + str(self.edad_minima) + "-" + str(self.edad_maxima)


class HorarioActividadesEscuela(models.Model):
    sede = models.ForeignKey(EscuelaDeportiva)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    dias = models.ManyToManyField(Dias, verbose_name='Días')
    descripcion = models.TextField(max_length=1024, verbose_name='Descripción')
    fecha_creacion = models.DateTimeField(auto_now_add=True)


class Participante(models.Model):
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
    genero = models.CharField(choices=tipo_sexo, max_length=11, verbose_name='Género del Participante')
    fecha_nacimiento = models.DateField(verbose_name='Fecha de nacimiento')
    tipo_id = models.CharField(max_length=10, choices=TIPO_IDENTIDAD, default='TI',
                               verbose_name='Tipo de Identificación')
    identificacion = models.CharField(max_length=100, verbose_name='Identificación')
    talla = models.IntegerField(verbose_name="Estatura (cm)")
    peso = models.IntegerField(verbose_name="Peso (Kg)")
    ciudad_residencia = models.ForeignKey(Ciudad, verbose_name='Ciudad de residencia')
    institucion_educativa = models.CharField(max_length=255, verbose_name="Institución educativa actual")
    anho_curso = models.CharField(max_length=100, choices=CURSO, verbose_name="Año que cursa actualmente")
    telefono = models.CharField(max_length=100, verbose_name='Teléfono')
    direccion = models.CharField(max_length=100, verbose_name='Dirección de residencia')
    nacionalidad = models.ManyToManyField(Nacionalidad, verbose_name='Nacionalidad')
    eps = models.ForeignKey(EPS, verbose_name='Sistema de salud afiliado')
    entidad = models.ForeignKey(Entidad)
    etnia = models.CharField(max_length=20, choices=ETNIAS, blank=True)
    sede_perteneciente = models.ForeignKey(EscuelaDeportiva, verbose_name="Sede a la que pertenece")
    categoria = models.ForeignKey(CategoriaEscuela, null=True, verbose_name="Categoría")
    estado = models.IntegerField(default=1, choices=ESTADO)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('tipo_id', 'identificacion',)
        permissions = (
            ("view_deportista", "Permite ver participante"),
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

    def get_estado_accion(self):
        return ("desactivado", "activado")[int(self.estado)]

    def save(self, *args, **kwargs):
        self.nombres = self.nombres.upper()
        self.apellidos = self.apellidos.upper()
        self.direccion = self.direccion.upper()
        super(Participante, self).save(*args, **kwargs)


class SeguimientoTallaPeso(models.Model):
    participante = models.ForeignKey(Participante)
    fecha_registro = models.DateField(auto_now_add=True)
    talla = models.IntegerField(verbose_name="Estatura (cm)")
    peso = models.IntegerField(verbose_name="Peso (Kg)")


class AlertaTemprana(models.Model):
    NIVEL_DE_ALERTA = (
        (0, "BAJA"),
        (1, "MEDIA"),
        (2, "ALTA"),
    )

    nivel_alerta = models.IntegerField(choices=NIVEL_DE_ALERTA, verbose_name="Nivel de alerta")
    referencia_alerta = models.CharField(max_length=150, verbose_name="Referencia de alerta")
    descripcion = models.TextField(verbose_name="Descripción", max_length=500)
    fecha_registro = models.DateField(auto_now_add=True)
    fecha_ultima_actualizacion = models.DateField(auto_now=True, null=True)
    estado = models.IntegerField(default=1, choices=ESTADO)
    participante = models.ForeignKey(Participante)

    def get_estado_accion(self):
        return ("desactivada", "activada")[int(self.estado)]


class Acudiente(models.Model):
    nombres = models.CharField(max_length=100, verbose_name='Nombres')
    apellidos = models.CharField(max_length=100, verbose_name='Apellidos')
    genero = models.CharField(choices=tipo_sexo, max_length=11, verbose_name='Genero del Participante')
    fecha_nacimiento = models.DateField(verbose_name='Fecha de nacimiento')
    tipo_id = models.CharField(max_length=10, choices=TIPO_IDENTIDAD, default='TI',
                               verbose_name='Tipo de Identificación')
    identificacion = models.CharField(max_length=100, verbose_name='Identificación')
    soporte_id = models.FileField(upload_to="soporte_acudientes_EFD",
                                  verbose_name="Soporte de identificación (escaneado)", null=True, blank=True)
    eps = models.ForeignKey(EPS, verbose_name='Sistema de salud afiliado')
    estado = models.IntegerField(default=1, choices=ESTADO)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    participante_responsable = models.ForeignKey(Participante)

    class Meta:
        unique_together = ('tipo_id', 'identificacion',)

    def full_name(self):
        return str(self.nombres) + " " + str(self.apellidos)

    def get_estado_accion(self):
        return ("desactivado", "activado")[int(self.estado)]


class ActividadEFD(models.Model):
    DIRIGIDO = (
        (0, "ACUDIENTES"),
        (1, "PARTICIPANTES"),
    )

    dirigido_a = models.IntegerField(choices=DIRIGIDO)
    sede = models.ForeignKey(EscuelaDeportiva)
    titulo = models.CharField(max_length=155, verbose_name="Título de actividad")
    descripcion = models.TextField(verbose_name="Descripción", max_length=500)
    dia_actividad = models.DateField(verbose_name="Día actividad")
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    participantes = models.ManyToManyField(Participante)
    acudientes = models.ManyToManyField(Acudiente)
    estado = models.IntegerField(choices=ESTADO, default=1)

    def get_estado_accion(self):
        return ("desactivada", "activada")[int(self.estado)]
