INSERT INTO indervalle.snd_dirigente (id, tipo_identificacion, identificacion, nombres, apellidos, genero, cargo, telefono, email, fecha_posesion, fecha_retiro, foto, descripcion, entidad_id, superior_id, estado) VALUES
  (1000, 'CC', '123456', 'PEDRO', 'BERMUDEZ CANO', 'Hombre', 'Presidente', '3333333', 'pedro@example.com', '2010-05-03', '2014-08-15', '', 'Descripción de Pedro', 1, NULL, 1),
  (1001, 'CC', '123458', 'PATRICIA', 'ARANDA NUÑEZ', 'Mujer', 'Vicepresidente', '5555555', 'patricia@example.com', '2010-03-08', '2014-10-15', '', 'Descripción de Patricia', 1, 1000, 1),
  (1002, 'CE', '123457', 'MARIANA', 'PUERTA GUTIERREZ', 'Mujer', 'Gerente', '4444444', 'mariana@example.com', '2010-05-03', '2014-08-15', '', 'Descripción de Mariana', 1, 1001, 1),
  (1003, 'CC', '123459', 'LEONARDO', 'PIDRAHITA CANO', 'Hombre', 'Contador', '6666666', 'leonardo@example.com', '2011-01-03', '2013-08-15', '', 'Descripción de Leonardo', 1, 1002, 1),
  (1004, 'PT', '123455', 'SEBASTIAN', 'SUAREZ RENGIFO', 'Hombre', 'Vocero', '7777777', 'sebastian@example.com', '2010-05-22', '2015-02-15', '', 'Descripción de Sebastian', 1, 1002, 1);

INSERT INTO indervalle.snd_dirigente_nacionalidad (id, dirigente_id, nacionalidad_id) VALUES
  (1000, 1000, 52),
  (1001, 1001, 53),
  (1002, 1002, 51),
  (1003, 1003, 52),
  (1004, 1001, 52);

INSERT INTO indervalle.snd_funcion (descripcion, dirigente_id) VALUES
  ('Función uno', 1000),
  ('Función dos', 1000),
  ('Función tres', 1000),
  ('Función uno', 1001),
  ('Función dos', 1001),
  ('Función tres', 1001),
  ('Función uno', 1002),
  ('Función dos', 1002),
  ('Función tres', 1002),
  ('Función uno', 1003),
  ('Función dos', 1003),
  ('Función tres', 1003),
  ('Función uno', 1004),
  ('Función dos', 1004),
  ('Función tres', 1004);
