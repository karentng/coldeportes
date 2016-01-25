from snd.models import *

'''
(
    (
        MODELO,
        [CAMPOS A FILTRAR/DESPLEGAR],
        [CAMPOS A DESPLEGAR],
        [['COLUMNA',[[COMPARACION, ESTILO]+]]]|None,
        [
            [
                NOMBRE A DESPLEGAR,
                URL,
                [PARAMETROS DEL URL],
                IMAGEN FA,
                [
                    [
                        [(campo)+],
                        [(valorCampo)+],
                        funcionDeEvaluacion
                    ]+
                ] | None
            ]+ | []
        ],
        False | True            -> Se consulta en todos los tenants o no
    ),
)
'''

MODELOS_DE_DATOS = (
    (   #Numero de modelo 0
        PersonalApoyo,
        ['nombres','apellidos','actividad', 'entidad'],
        ['Nombres','Apellidos','Actividad Desempeñada', 'Entidad'],
        None,
        [
            [
                "Ver más",
                'ver_personal_apoyo_tenantnacional',
                ['id','entidad.id'],
                'fa-eye',
                None
            ],
        ],
    ),
    (   #Numero de modelo 1
        Dirigente,
        ['nombres','apellidos', 'entidad', 'cargo'],
        ['Nombres','Apellidos', 'Entidad', 'Cargo'],
        None,
        [
            [
                "Ver más",
                'ver_dirigente_tenantnacional',
                ['id','entidad.id'],
                'fa-eye',
                None
            ],
        ],
    ),
    (   #Numero de modelo 2
        Escenario,
        ['nombre','ciudad', 'entidad'],
        ['Nombre','Ciudad(Departamento)', 'Entidad'],
        None,
        [
            [
                "Ver más",
                'ver_escenario_tenantnacional',
                ['id','entidad.id'],
                'fa-eye',
                None
            ],
        ],
    ),
    
    (   #Numero de modelo 3
        Deportista,
        ['nombres','apellidos', 'entidad', 'ciudad_residencia','disciplinas'],
        ['Nombres','Apellidos', 'Entidad', 'Ciudad(Departamento) Residencia', 'Disciplinas'],
        None,
        [
            [
                "Ver más",
                'ver_deportista_tenantnacional',
                ['id','entidad.id','estado'],
                'fa-eye',
                None
            ],
        ],
    ),
    (   #Numero de modelo 4
        CentroAcondicionamiento,
        ['nombre', 'ciudad', 'entidad', 'telefono', 'email', 'web'],
        ['Nombre', 'Ciudad', 'Entidad', 'Teléfono', 'Email', 'Página Web'],
        None,
        [
            [
                "Ver más",
                'ver_caf_tenantnacional',
                ['id','entidad.id'],
                'fa-eye',
                None
            ],
        ],
    ),
)
