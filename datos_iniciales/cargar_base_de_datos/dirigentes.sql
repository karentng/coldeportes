INSERT INTO indervalle.snd_dirigente (id, tipo_identificacion, identificacion, nombres, apellidos, genero, telefono, email, foto, perfil, entidad_id, estado, ciudad_residencia_id) VALUES
  (1000, 'CC', '123456', 'PEDRO', 'BERMUDEZ CANO', 'Hombre', '3333333', 'pedro@example.com', '', 'Descripción de Pedro', 1, 0, 1),
  (1001, 'CC', '123458', 'PATRICIA', 'ARANDA NUÑEZ', 'Mujer', '5555555', 'patricia@example.com', '', 'Descripción de Patricia', 1, 0, 2),
  (1002, 'CE', '123457', 'MARIANA', 'PUERTA GUTIERREZ', 'Mujer', '4444444', 'mariana@example.com', '', 'Descripción de Mariana', 1, 0, 3),
  (1003, 'CC', '123459', 'LEONARDO', 'PIDRAHITA CANO', 'Hombre', '6666666', 'leonardo@example.com', '', 'Descripción de Leonardo', 1, 0, 4),
  (1004, 'PT', '123455', 'SEBASTIAN', 'SUAREZ RENGIFO', 'Hombre', '7777777', 'sebastian@example.com', '', 'Descripción de Sebastian', 1, 0, 5);

INSERT INTO indervalle.snd_dirigente_nacionalidad (id, dirigente_id, nacionalidad_id) VALUES
  (1000, 1000, 52),
  (1001, 1001, 53),
  (1002, 1002, 51),
  (1003, 1003, 52),
  (1004, 1004, 52);

INSERT INTO indervalle.snd_dirigentecargo (id, nombre, fecha_posesion, fecha_retiro, superior_id, superior_cargo_id, dirigente_id) VALUES
 (1000,'Presidente','01-01-2010','31-12-2010',NULL,NULL,1000),
 (1001,'Presidente','01-01-2011','31-12-2012',NULL,NULL,1000),
 (1008,'Presidente','01-01-2013','28-12-2015',NULL,NULL,1003),
 (1002,'Vicepresidente','01-01-2013','31-12-2013',1003,1008,1000),
 (1003,'Vicepresidente','01-01-2014','28-12-2015',1003,1008,1001),
 (1004,'Gerente','01-01-2014','06-08-2014',1001,1003,1002),
 (1005,'Contador','29-12-2015','03-03-2016',1001,1003,1003),
 (1006,'Vocero','01-01-2014','06-08-2014',1002,1004,1004),
 (1007,'Asistente','01-01-2016','03-03-2016',1003,1005,1004);

INSERT INTO indervalle.snd_dirigentefuncion (descripcion, dirigente_id, cargo_id) VALUES
  ('Función uno', 1000,1000),
  ('Función dos', 1000,1000),
  ('Función tres', 1000,1000),
  ('Función uno', 1001,1001),
  ('Función dos', 1001,1001),
  ('Función tres', 1001,1001),
  ('Función uno', 1002,1002),
  ('Función dos', 1002,1003),
  ('Función tres', 1002,1004),
  ('Función uno', 1003,1005),
  ('Función dos', 1003,1006),
  ('Función tres', 1003,1006),
  ('Función uno', 1004,1007),
  ('Función dos', 1004,1008),
  ('Función tres', 1004,1008);