INSERT INTO indervalle.snd_centroacondicionamiento (id, nombre, direccion, telefono, email, ciudad_id, comuna, barrio, estrato, latitud, longitud, altura, nombre_administrador, contacto, estado, entidad_id) VALUES
(10000, 'ANGELES GYM CAPF', 'Cl 13 B 85C – 75 Ingenio I', '330 45 91 – 321 763 56 69', 'angeles@gmail.com', 152, 21, 'INGENIO', 5, 10, 10, 10, 'JUAN ALBERTO CASTAÑEDA', 'LLAMAR AL NÚMERO DE TELEFONO', 1, 1);

INSERT INTO indervalle.snd_centroacondicionamiento_clases(centroacondicionamiento_id, caclase_id) VALUES
(10000, 40),
(10000, 30),
(10000, 20),
(10000, 10),
(10000, 5),
(10000, 2),
(10000, 1);

INSERT INTO indervalle.snd_centroacondicionamiento_servicios(centroacondicionamiento_id, caservicio_id) VALUES
(10000, 9),
(10000, 5),
(10000, 3),
(10000, 2),
(10000, 1);

INSERT INTO indervalle.snd_caplan(nombre, precio, descripcion, centro_id) VALUES
('PLAN DIAMANTE', 100000, 'TODO INCLUIDO', 10000),
('PLAN PLATINO', 90000, 'ENTRENOS, ASESORIAS, CURSOS Y SEMINARIOS', 10000),
('PLAN PLATA', 100000, 'ENTRENOS Y ASESORIAS', 10000),
('PLAN BRONCE', 100000, 'ENTRENOS', 10000);