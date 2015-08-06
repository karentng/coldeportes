python3 ../manage.py dbshell < datos_iniciales.sql
python3 ../manage.py dbshell < tipo_superficie.sql
python3 ../manage.py dbshell < datos_iniciales_cafs.sql
python3 ../manage.py dbshell < cajas_compensacion.sql

python3 ../manage.py dbshell < cargar_base_de_datos/escenarios.sql
python3 ../manage.py dbshell < cargar_base_de_datos/cafs.sql
python3 ../manage.py dbshell < cargar_base_de_datos/deportistas.sql
python3 ../manage.py dbshell < cargar_base_de_datos/dirigentes.sql
python3 ../manage.py dbshell < cargar_base_de_datos/entrenadores.sql