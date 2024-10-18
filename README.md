# APARTAT 1
# En este apartado lo que se pide es que se muestre una tabla de los 
# alumnos: 

# FICHERO SCRIPT.JS:
# Primero se hace con un fetch llamando al endpoint de la API. 
# Después de eso tenemos que poner la iteración de cada campo que 
# queremos pasarle para que se muestre en la tabla. 

# FICHERO DB_ALUMNES.PY
# Como uno de los campos que pide pertenece a la tabla de Aula y no a la 
# misma tabla de Alumne, tenemos que hacer un join en el fichero 
# db_alumnes.py en la función adecuada. 

# FICHERO ALUMNES.PY
# Además tenemos que cambiar los campos que le pasamos en la función del 
# alumno para que nos coja los 5 campos que necesitamos. 

# FICHERO MAIN.PY
# En este fichero se tiene que añadir un import que sirve para que el 
# frontend que tiene un codigo de Javascript se pueda comunicar con el 
# backend. Además tenemos que añadir unas lineas que pertenecen a ese 
# import para que pueda ejecutarse bien. Creamos una clase Base que 
# contenga los campos que devuelve el select de la tabla de alumnos. 
# Después de añadir los campos necesarios y hacer los cambios necesarios 
# ejecutamos el archivo de index.html y nos tiene que salir la tabla 
# completa (teniendo en cuenta que no salen los nuevos alumnos del 
# apartado 3):

# ![alt text](img/tabla_alumnos_html.png)
# Con los alumnos añadidos del apartado 3:
# ![alt text](img/tabla_alumnos_html_completo.png)


# APARTAT 2

# orderby
# ![alt text](img/orderby.png)
# ![alt text](img/docs_orderby.png)


# contain
# ![alt text](img/contain_no.png)
# ![alt text](img/contain_yes.png)
# ![alt text](img/docs_contains.png)
# ![alt text](img/docs_contains_no.png)

# skip i limit
# ![alt text](img/skip_limit.png)
# ![alt text](img/skip_limit_tot.png)

# Tot junt
# amb orderby = asc, skip = 0 y limit = 5:
# ![alt text](img/tot.png)
# ![alt text](img/docs_tot.png)


# Apartat 3
# ![alt text](img/arxiu_csv.png)
# ![alt text](img/csv_no.png)
# Les taules canvien:
# ![alt text](img/taula_alumn.png)
# ![alt text](img/taula_aula.png)
