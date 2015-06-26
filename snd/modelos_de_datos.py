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
        ['nombre','direccion', 'telefono', 'ciudad', 'estado'],
        ['Nombre','Dirección', 'Teléfono', 'Ciudad', 'Estado'],
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
                "Modificar",
                'modificar_caf',
                ['id'],
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