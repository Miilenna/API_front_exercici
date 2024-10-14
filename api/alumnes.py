#Función que convierte la información de un registro de la tabla "alumne" en un diccionario
def alumne_schema(fetchAlumnes) -> dict:
    return {"NomAlumne": fetchAlumnes[0],
            "Cicle": fetchAlumnes[1],
            "Curs": fetchAlumnes[2],
            "Grup": fetchAlumnes[3],
            "DescAula": fetchAlumnes[4]
            }
#Función que convierte la información de un registro de la tabla "aula" en un diccionario
def aula_schema(aules) -> dict:
    return {
        "idAula": aules[0],
        "DescAula": aules[1],
        "Edifici": aules[2],
        "Pis":aules[3],
        "CreateAt":aules [4],
        "UpdatedAt":aules[5]
    }

#Función que convierte una lista de registros de la tabla "aula" en una lista de diccionarios
def aules_schema(aules) -> dict:
    #Itera sobre cada registro de "aula" y lo transforma en un diccionario
    return [aula_schema(aula) for aula in aules]

#Función que convierte una lista de registros de la tabla "alumne" en una lista de diccionarios
def alumnes_schema(fetchAlumnes) -> dict:
    #Itera sobre cada registro de "alumne" y lo transforma en un diccionario
    return [alumne_schema(alumne) for alumne in fetchAlumnes]