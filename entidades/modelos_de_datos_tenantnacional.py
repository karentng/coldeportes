from entidades.modelos_vistas_reportes import *

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
    ),
)
'''

MODELOS_DE_DATOS = (
    (   #Numero de modelo 0
        PublicPersonalApoyoView,
        ['nombres','apellidos','actividad', 'ciudad', 'entidad'],
        ['Nombres','Apellidos','Actividad Desempeñada', 'Ciudad', 'Entidad'],
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
        PublicDirigenteView,
        ['nombres','apellidos', 'ciudad', 'entidad'],
        ['Nombres','Apellidos', 'Ciudad', 'Entidad'],
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
        PublicEscenarioView,
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
        PublicDeportistaView,
        ['nombres','apellidos', 'ciudad_residencia', 'entidad'],
        ['Nombres','Apellidos', 'Ciudad(Departamento) Residencia', 'Entidad'],
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
        PublicCafView,
        ['nombre', 'ciudad', 'telefono', 'email', 'web', 'entidad'],
        ['Nombre', 'Ciudad', 'Teléfono', 'Email', 'Página Web', 'Entidad'],
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
    (   #Numero de modelo 5
        PublicEscuelaView,
        ['nombre', 'ciudad', 'tipo_sede', 'telefono_fijo', 'email', 'web', 'estrato','entidad'],
        ['Nombre', 'Ciudad', 'Tipo Sede', 'Teléfono', 'Email', 'Página Web', 'Estrato', 'Entidad'],
        None,
        [
            [
                "Ver más",
                'ver_escuelas_tenantnacional',
                ['id','entidad.id'],
                'fa-eye',
                None
            ],
        ],
    ),
    (   #Numero de modelo 6
        PublicCajasView,
        ['nombre', 'ciudad', 'clasificacion','email','entidad'],
        ['Nombre', 'Ciudad', 'Clasificación','Email','Entidad'],
        None,
        [
            [
                "Ver más",
                'ver_cajas_tenantnacional',
                ['id','entidad.id'],
                'fa-eye',
                None
            ],
        ],
    ),
)
