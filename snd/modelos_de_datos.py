import operator
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
    ),
)
'''

MODELOS_DE_DATOS = (
    #0
    (
        CentroAcondicionamiento,
        ['nombre','direccion', 'telefono', 'ciudad', 'email', 'web', 'estado'],
        ['Nombre','Dirección', 'Teléfono', 'Ciudad', 'Email', 'Página Web', 'Estado'],
        None,
        [
            [
                "Ver CAF",
                'ver_caf',
                ['id','entidad.id'],
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
        ],
    ),
    #1
    #MODELO DE DATOS CAF PARA LIGAS Y FEDERACIONES
    (
        CentroAcondicionamiento,
        ['nombre','direccion', 'telefono', 'ciudad', 'email', 'web', 'entidad'],
        ['Nombre','Dirección', 'Teléfono', 'Ciudad', 'Email', 'Página Web', 'Entidad'],
        None,
        [
            [
                "Ver CAF",
                'ver_caf',
                ['id','entidad.id'],
                'fa-eye',
                None
            ],
        ],
    ),
    #2
    (
        Deportista,
        ["foto","nombres apellidos","ciudad_residencia","tipo_id","identificacion","estado"],
        ["Foto","Nombre","Ciudad de residencia","Tipo Identificación","Identificación","Estado"],
        None,
        [
            [
                "Ver Deportista",
                'ver_deportista',
                ['id','entidad.id'],
                'fa-eye',
                None
            ],
            [
                "Editar",
                'edicion_deportista',
                ['id'],
                'fa-gear',
                [
                    [
                        ['estado'],
                        ['ACTIVO'],
                        lambda x, y: operator.eq(x[0], y[0])
                    ]
                ]

            ],
            [
                "CTD",
                'cambio_documento_deportista',
                ['id'],
                'fa-archive',
                [
                    [
                        ['estado'],
                        ['ACTIVO'],
                        lambda x, y: operator.eq(x[0], y[0])
                    ]
                ]

            ],
            [
                "A/I",
                'deportista_desactivar',
                ['id'],
                'fa-ban',
                [
                    [
                        ['estado'],
                        ['ACTIVO','INACTIVO'],
                        lambda x, y: operator.eq(x[0], y[0]) or operator.eq(x[0], y[1])
                    ]
                ]

            ],
            [
                "Transferir",
                'generar_transferencia',
                ['id'],
                'fa-exchange',
                [
                    [
                        ['estado'],
                        ['ACTIVO'],
                        lambda x, y: operator.eq(x[0], y[0])
                    ]
                ]

            ],
            [
                "Cancelar Transferencia",
                'cancelar_transferencia',
                ['id'],
                'fa-times',
                [
                    [
                        ['estado'],
                        ['EN TRANSFERENCIA'],
                        lambda x, y: operator.eq(x[0], y[0])
                    ]
                ]

            ],

        ],
    ),
    #3
    #MODELO DE DATOS PARA DEPORTISTAS PARA EL TENANT TIPO LIGA Y FEDERACIÓN
    (
        Deportista,
        ["foto","nombres apellidos","ciudad_residencia","tipo_id","identificacion","entidad"],
        ["Foto","Nombre","Ciudad de residencia","Tipo Identificación","Identificación","Entidad"],
        None,
        [
            [
                "Ver Deportista",
                'ver_deportista',
                ['id','entidad.id'],
                'fa-eye',
                None
            ]
        ],
    ),
    #4
    (
        PersonalApoyo,
        ['foto','nombres apellidos', 'actividad', 'identificacion', 'estado'],
        ['Foto','Nombre', 'Actividad desempeñada', 'Identificación', 'Estado'],
        None,
        [
            [
                "Ver más",
                'ver_personal_apoyo',
                ['id','entidad.id'],
                'fa-eye',
                None
            ],
            [
                "Editar",
                'edicion_personal_apoyo',
                ['id'],
                'fa-gear',
                None
            ],
            [
                "A/I",
                'personal_apoyo_desactivar',
                ['id'],
                'fa-ban',
                [
                    [
                        ['estado'],
                        ['ACTIVO','INACTIVO'],
                        lambda x, y: operator.eq(x[0], y[0]) or operator.eq(x[0], y[1])
                    ]
                ]

            ],
        ],
    ),
    #5
    #MODELO DE DATOS PARA PERSONAL DE APOYO PARA FEDERACIONES Y LIGAS
    (
        PersonalApoyo,
        ['foto','nombres apellidos', 'actividad', 'identificacion', 'entidad'],
        ['Foto','Nombre', 'Actividad desempeñada', 'Identificación', 'Entidad'],
        None,
        [
            [
                "Ver más",
                'ver_personal_apoyo',
                ['id','entidad.id'],
                'fa-eye',
                None
            ],
            [
                "Editar",
                'edicion_personal_apoyo',
                ['id'],
                'fa-gear',
                None
            ],
            [
                "A/I",
                'personal_apoyo_desactivar',
                ['id'],
                'fa-ban',
                [
                    [
                        ['estado'],
                        ['ACTIVO','INACTIVO'],
                        lambda x, y: operator.eq(x[0], y[0]) or operator.eq(x[0], y[1])
                    ]
                ]

            ]
        ],
    ),
    #6
    (
        Dirigente,
        ['foto','identificacion','nombres apellidos', 'estado'],
        ['Foto','Identificación','Nombre', 'Estado'],
        None,
        [
            [
                "Ver más",
                'dirigentes_ver',
                ['id','entidad.id'],
                'fa-eye',
                None
            ],
            [
                "Editar",
                'dirigentes_wizard_identificacion',
                ['id'],
                'fa-gear',
                None
            ],
            [
                "A/I",
                'dirigentes_activar_desactivar',
                ['id'],
                'fa-ban',
                [
                    [
                        ['estado'],
                        ['ACTIVO','INACTIVO'],
                        lambda x, y: operator.eq(x[0], y[0]) or operator.eq(x[0], y[1])
                    ]
                ]

            ]
        ],
    ),
    #7
    #MODELO DE DATOS DIRIGENTE PARA LIGA Y FEDERACIÓN
    (
        Dirigente,
        ['foto','identificacion','nombres apellidos', 'entidad'],
        ['Foto','Identificación','Nombre', 'Entidad'],
        None,
        [
            [
                "Ver más",
                'dirigentes_ver',
                ['id','entidad.id'],
                'fa-eye',
                None
            ],
            [
                "Editar",
                'dirigentes_wizard_identificacion',
                ['id'],
                'fa-gear',
                None
            ],
            [
                "A/I",
                'dirigentes_activar_desactivar',
                ['id'],
                'fa-ban',
                [
                    [
                        ['estado'],
                        ['ACTIVO','INACTIVO'],
                        lambda x, y: operator.eq(x[0], y[0]) or operator.eq(x[0], y[1])
                    ]
                ]

            ]
        ],
    ),
    #8
    (
        Escenario,
        ['nombre','ciudad','estrato', 'estado'],
        ['Nombre','Ciudad(Departamento)','Estrato', 'Estado'],
        None,
        [
            [
                "Ver más",
                'ver_escenario',
                ['id','entidad.id'],
                'fa-eye',
                None
            ],
            [
                "Editar",
                'wizard_identificacion',
                ['id'],
                'fa-gear',
                [
                    [
                        ['estado'],
                        ['ACTIVO'],
                        lambda x, y: operator.eq(x[0], y[0])
                    ]
                ]
            ],
            [
                "A/I",
                'desactivar_escenario',
                ['id'],
                'fa-ban',
                [
                    [
                        ['estado'],
                        ['ACTIVO','INACTIVO'],
                        lambda x, y: operator.eq(x[0], y[0]) or operator.eq(x[0], y[1])
                    ]
                ]

            ]
        ],
    ),
    #9
    #MODELO DE DATOS PARA ESCENARIO LIGAS Y FEDERACIONES
    (
        Escenario,
        ['nombre','ciudad','estrato', 'entidad'],
        ['Nombre','Ciudad(Departamento)','Estrato', 'Entidad'],
        None,
        [
            [
                "Ver más",
                'ver_escenario',
                ['id','entidad.id'],
                'fa-eye',
                None
            ],
        ],
    ),
    #10
    (
        Seleccion,
        ["nombre", "tipo", "fecha_inicial", "fecha_final", "campeonato", "tipo_campeonato"],
        ["Nombre", "Tipo de Selección", "Fecha Convocatoria", "Fecha Finaliza Convocatoria", "Nombre Campeonato", "Tipo Campeonato"],
        None,
        [
            [
                "Ver Seleccion",
                'ver_seleccion',
                ['id'],
                'fa-eye',
                None
            ],
            [
                "Editar",
                'editar_seleccion',
                ['id'],
                'fa-gear',
                None
            ],
        ],
    ),
    #11
    #MODELO PARA CLUB PARALIMPICO
    (
        Deportista,
        ["foto","nombres apellidos","ciudad_residencia","tipo_id","identificacion","estado"],
        ["Foto","Nombre","Ciudad de residencia","Tipo Identificación","Identificación","Estado"],
        None,
        [
            [
                "Ver Deportista",
                'ver_deportista',
                ['id','entidad.id'],
                'fa-eye',
                None
            ],
            [
                "Editar",
                'edicion_deportista',
                ['id'],
                'fa-gear',
                [
                    [
                        ['estado'],
                        ['ACTIVO'],
                        lambda x, y: operator.eq(x[0], y[0])
                    ]
                ]

            ],
            [
                "CTD",
                'cambio_documento_deportista',
                ['id'],
                'fa-archive',
                [
                    [
                        ['estado'],
                        ['ACTIVO'],
                        lambda x, y: operator.eq(x[0], y[0])
                    ]
                ]

            ],
            [
                "A/I",
                'deportista_desactivar',
                ['id'],
                'fa-ban',
                [
                    [
                        ['estado'],
                        ['ACTIVO','INACTIVO'],
                        lambda x, y: operator.eq(x[0], y[0]) or operator.eq(x[0], y[1])
                    ]
                ]

            ],

        ],
    ),
    #12
    (
        CentroBiomedico,
        ['nombre','direccion', 'telefono_fijo', 'ciudad', 'email', 'web', 'estado'],
        ['Nombre','Dirección', 'Teléfono', 'Ciudad', 'Email', 'Página Web', 'Estado'],
        None,
        [
            [
                "Ver Centro Biomédico",
                'centro_biomedico_ver',
                ['id','entidad.id'],
                'fa-eye',
                None
            ],
            [
                "Editar",
                'centro_biomedico_crear_editar',
                ['identificacion', '1', 'id'],
                'fa-gear',
                None
            ],
        ],
    ),
)
