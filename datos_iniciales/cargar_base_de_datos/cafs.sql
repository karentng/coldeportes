INSERT INTO indervalle.snd_centroacondicionamiento (id, nombre, direccion, telefono, email, web, nombre_administrador, ciudad_id, comuna, barrio, estrato, latitud, longitud, altura, estado, entidad_id) VALUES
(10000, 'ANGELES GYM CAPF', 'Cl 13 B 85C – 75 Ingenio I', '330 45 91 – 321 763 56 69', 'angeles@gmail.com', 'http://angelesgym.co/', 'JUAN ALBERTO CASTAÑEDA', 152, 21, 'INGENIO', 5, 10, 10, 10, 0, 1),

(10001, 'MUSCULOSOS GYM', 'Cl 129 A 96B – 75', '392 9999', 'musculosos@gmail.com', 'http://musculososgym.co/', 'MARIO ALBERTO MUSCULOS', 152, 21, 'BARRIO MUSCULOS', 6, 11, 11, 11, 0, 1),

(10002, 'ATHLETIC FITNESS', 'CR 66 # 2C-46', '324 4040', 'info@athleticgym.co', 'http://athleticgym.co/', 'JUANITO', 152, 21, 'REFUGIO', 5, 12, 12, 12, 0, 1);

INSERT INTO indervalle.snd_centroacondicionamiento_clases(centroacondicionamiento_id, caclase_id) VALUES
(10000, 40),
(10000, 30),
(10000, 20),
(10000, 10),
(10000, 5),
(10000, 2),
(10000, 1),

(10001, 36),
(10001, 24),
(10001, 12),
(10001, 6),
(10001, 4),
(10001, 2),

(10002, 35),
(10002, 25),
(10002, 15),
(10002, 5),
(10002, 1);

INSERT INTO indervalle.snd_centroacondicionamiento_servicios(centroacondicionamiento_id, caservicio_id) VALUES
(10000, 9),
(10000, 5),
(10000, 3),
(10000, 2),
(10000, 1),

(10001, 8),
(10001, 7),
(10001, 6),
(10001, 4),
(10001, 1),

(10002, 9),
(10002, 8),
(10002, 6),
(10002, 5),
(10002, 1);

INSERT INTO indervalle.snd_caplan(nombre, precio, descripcion, centro_id) VALUES
('PLAN DIAMANTE', 100000, 'TODO INCLUIDO', 10000),
('PLAN PLATINO', 90000, 'ENTRENOS, ASESORIAS, CURSOS Y SEMINARIOS', 10000),
('PLAN PLATA', 100000, 'ENTRENOS Y ASESORIAS', 10000),
('PLAN BRONCE', 100000, 'ENTRENOS', 10000);