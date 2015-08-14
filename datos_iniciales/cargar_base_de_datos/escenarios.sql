INSERT INTO indervalle.snd_escenario ("id", "nombre", "direccion", "latitud", "longitud", "altura", "comuna", "barrio", "estrato", "nombre_administrador", "descripcion", "ciudad_id", "entidad_id", "estado") VALUES
(3,	'PASCUAL GUERRERO',	'CALLE 5 # 32-54',	6.05,	5.01,	3.25,	'10',	'SAN FERNANDO',	'4',	'JOSE TULIO RODRIGUEZ',	'Estadio de fútbol y pista de atletismo.',	152,	2,	0),
(2,	'COLISEO EVANGELISTA MORA',	'CALLE 23 # 33A 04',	1,	1.45,	230,	'10',	'SAN FERNANDO',	'2',	'JOSE PEREZ',	'Ubicado en la zona oriente de Cali.',	152,	2,	0),
(4,	'DIABLO AZTECA',	'CALLE 13 # 57-12',	7,	8,	300,	'3',	'INGENIO',	'5',	'JUAN CARLOS RODRIGUEZ',	'Cancha sintética',	152,	2,	0);

INSERT INTO indervalle.snd_caracterizacionescenario (id, capacidad_espectadores, metros_construidos, clase_acceso, descripcion, escenario_id, tipo_escenario_id) VALUES
(2,	'1500 personas en tribuna, 400 en palcos',	'350 metros en cemento',	'pcp',	'El estadio se encuentra en buenas condiciones de obra. ',	3,	1),
(1,	'500',	'1500',	'dul',	'Coliseo recubierto en buen estado de obra.',	2,	6),
(3,	'150',	'200',	'pr',	'Cancha para Recreación y Esparcimiento.',	4,	6);

INSERT INTO indervalle.snd_caracterizacionescenario_caracteristicas (id, caracterizacionescenario_id, caracteristicaescenario_id) VALUES
(15,	2,	2),
(16,	2,	3),
(17,	2,	22),
(18,	1,	21),
(19,	1,	22),
(20,	3,	3),
(21,	3,	22);

INSERT INTO indervalle.snd_caracterizacionescenario_clase_uso (id, caracterizacionescenario_id, tipousoescenario_id) VALUES
(8,	2,	2),
(9,	1,	1),
(10,	3,	1);

INSERT INTO indervalle.snd_caracterizacionescenario_tipo_disciplinas (id, caracterizacionescenario_id, tipodisciplinadeportiva_id) VALUES
(15,	2,	4),
(16,	2,	6),
(17,	1,	2),
(18,	3,	4);

INSERT INTO indervalle.snd_caracterizacionescenario_tipo_superficie_juego (id, caracterizacionescenario_id, tiposuperficie_id) VALUES
(9,	2,	2),
(10,	1,	10),
(11,	3,	3);

INSERT INTO indervalle.snd_horariodisponibilidad (id, hora_inicio, hora_fin, descripcion, escenario_id) VALUES
(1,	'08:00:58',	'17:00:59',	'Horario de Atención ',	3),
(2,	'14:00:42',	'18:00:42',	'Horario de Taquilla',	3),
(3,	'04:00:35',	'09:00:35',	'Horario de Taquilla',	2),
(4,	'09:00:08',	'13:20:08',	'Horarios de Reservas',	4);

INSERT INTO indervalle.snd_horariodisponibilidad_dias (id, horariodisponibilidad_id, dias_id) VALUES
(1,	1,	2),
(2,	1,	3),
(3,	1,	4),
(4,	1,	5),
(5,	1,	6),
(6,	2,	2),
(7,	2,	3),
(8,	3,	3),
(9,	3,	4),
(10,	4,	5),
(11,	4,	6);


INSERT INTO indervalle.snd_datohistorico (id, fecha_inicio, fecha_fin, descripcion, escenario_id) VALUES
(1,	'2009-07-16',	'2010-07-13',	'Remodelación ',	3),
(2,	'2005-07-14',	'2015-07-12',	'Reconstruido e inaugurado.',	2),
(3,	'2015-07-03',	'2015-07-31',	'Inauguración',	4);

INSERT INTO indervalle.snd_contacto (id, nombre, telefono, email, escenario_id, descripcion) VALUES
(1,	'CARLOS RESTREPO',	'3156889515',	'cramirez@cali.gov.co',	3,	'Atención al cliente'),
(2,	'CLEMENCIA TORRES',	'35578212-2412',	'ctorres@evangelista.gov.co',	2,	'Contacto administrativo'),
(3,	'CARLOS SANCHEZ',	'3168849230',	'csanchez@gmail.com',	4,	'Reservas');