from django.db import models

# Create your models here.
class CasoDoping(models.Model):
    TIPO_IDENTIDAD = (
        ('CC', 'CÉDULA DE CIUDADANÍA'),
        ('TI', 'TARJETA DE IDENTIDAD'),
        ('CE', 'CÉDULA DE EXTRANJERÍA'),
        ('PS', 'PASAPORTE'),
    )

    ESTADOS = (
        (0,'ACTIVO'),
        (1,'INACTIVO'),
    )

    TIPO_SANCION = (
        (0, 'LA PRESENCIA DE UNA SUSTANCIA PROHIBIDA O DE SUS METABOLITOS O MARCADORES EN LA MUESTRA DE UN DEPORTISTA'),
        (1, 'USO O INTENTO DE USO POR PARTE DE UN DEPORTISTA DE UNA SUSTANCIA PROHIBIDA O DE UN MÉTODO PROHIBIDO'),
        (2, 'EVITAR, RECHAZAR O INCUMPLIR LA OBLIGACIÓN DE SOMETERSE A LA RECOGIDA DE MUESTRAS'),
        (3, 'INCUMPLIMIENTO DE LA LOCALIZACIÓN/PARADERO DEL DEPORTISTA'),
        (4, 'MANIPULACIÓN O INTENTO DE MANIPULACIÓN DE CUALQUIER PARTE DEL PROCESO DE CONTROL DE DOPAJE'),
        (5, 'POSESIÓN DE UNA SUSTANCIA PROHIBIDA O UN MÉTODO PROHIBIDO'),
        (6, 'TRÁFICO O INTENTO DE TRÁFICO DE CUALQUIER SUSTANCIA PROHIBIDA O MÉTODO PROHIBIDO'),
        (7, 'ADMINISTRACIÓN O INTENTO DE ADMINISTRACIÓN EN COMPETICIÓN A UN DEPORTISTA DE UNA SUSTANCIA PROHIBIDA O MÉTODO'
            ' PROHIBIDO O ADMINISTRACIÓN O INTENTO DE ADMINISTRACIÓN A CUALQUIER DEPORTISTA FUERA DE COMPETICIÓN DE CUALQUIER'
            ' SUSTANCIA PROHIBIDA O CUALQUIER MÉTODO PROHIBIDO QUE ESTÉ PROHIBIDO FUERA DE COMPETICIÓN'),
        (8, 'COMPLICIDAD'),
        (9, 'ASOCIACIÓN PROHIBIDA'),
    )
    nombres_deportista = models.CharField(max_length=100)
    apellidos_deportista = models.CharField(max_length=100)
    tipo_id = models.CharField(max_length=10, choices=TIPO_IDENTIDAD, default='CC',verbose_name='Tipo de Identificación')
    identificacion = models.CharField(max_length=100,verbose_name='Identificación')
    tipo_sancion = models.IntegerField(choices=TIPO_SANCION)
    duracion_sancion = models.CharField(max_length=255)
    estado = models.IntegerField(default=0)