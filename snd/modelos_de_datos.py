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
        ]
    ),
)
'''

MODELOS_DE_DATOS = (
    (
        CentroAcondicionamiento,
        ['nombre','direccion', 'telefono', 'ciudad', 'email', 'web', 'estado'],
        ['Nombre','Dirección', 'Teléfono', 'Ciudad', 'Email', 'Página Web', 'Estado'],
        None,
        [
            [
                "Ver CAF",
                'ver_caf',
                ['id'],
                'fa-eye',
                None
            ],
            [
                "Editar",
                'crear_caf',
                ['Identificación', 'id'],
                'fa-gear',
                None
            ],
        ]
    ),
)

'''
    [
        "Activar/Desactivar",
        'desactivar_caf',
        ['id'],
        'fa-ban',
        None
    ],
'''