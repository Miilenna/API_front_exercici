from client import db_client

#Función que muestra toda la información de la tabla "alumne"
def read_alumne(orderby : str = None, contain: str = None, skip: int = 0, limit: int | None = None ):
    try:
        #Conexión a la base de datos
        conn = db_client()
        cur = conn.cursor()
        #Consulta SQL para seleccionar todos los registros de la tabla "alumne"
        sql_query = """select alumne.NomAlumne, alumne.Cicle, alumne.Curs, alumne.Grup, aula.DescAula
                    from alumne
                    join aula on alumne.idAula = aula.idAula
                    """
        if (orderby == "asc"):
            sql_query += " ORDER BY alumne.NomAlumne ASC"
        elif (orderby == "desc"):
            sql_query += " ORDER BY alumne.NomAlumne DESC"
            
        if(contain):
            sql_query += " WHERE alumne.NomAlumne ILIKE %s"
        
        if(limit is not None):
            sql_query += " LIMIT %s"
            
        if(skip > 0):
            sql_query += " OFFSET %s"
        
        parametres = []
        if contain:
            parametres.append(f"%{contain}%")
        if limit is not None:
            parametres.append(limit)
        if skip > 0 and skip <= 100:
            parametres.append(skip)
            

        cur.execute(sql_query, parametres)

        #Almacena el resultado de la consulta
        select_alumne = cur.fetchall()
    
    except Exception as e:
        #Si hay un error devuelve un mensaje
        return {"status": -1, "message": f"Error de connexió:{e}" }
    
    finally:
        #Cierra la conexión hacia la base de datos
        conn.close()
    
    return select_alumne

#Función que muestra toda la información de la tabla "aula"
def readAula():
    try:
        conn = db_client()
        cur = conn.cursor()
        
        #Consulta SQL para seleccionar todos los registros de la tabla "aula"
        cur.execute("select * from aula")
    
        select_aula = cur.fetchall()
    
    except Exception as e:
        #Si hay un error devuelve un mensaje
        return {"status": -1, "message": f"Error de connexió:{e}" }
    
    finally:
        conn.close()
    
    return select_aula

#Función que muestra la información de un alumno en concreto pasándole su id
def read_id(idAlumne):
    try:
        conn = db_client()
        cur = conn.cursor()
       
        #Consulta SQL para seleccionar un alumno según su id
        query = "select * from alumne WHERE idAlumne = %s"
        value = (idAlumne,)
        cur.execute(query,value)
    
        select_id = cur.fetchone()

    except Exception as e:
        return {"status": -1, "message": f"Error de connexió:{e}" }
    
    finally:
        conn.close()
    
    return select_id

#Función que inserta un nuevo alumno en la tabla "alumne"
def create_alumne(idAula,NomAlumne,Cicle,Curs,Grup):
    try:
        conn = db_client()
        cur = conn.cursor()
        
        #Consulta SQL para insertar un nuevo alumno
        query = "insert into alumne (idAula,NomAlumne,Cicle,Curs,Grup) VALUES (%s,%s,%s,%s,%s);"
        values=(idAula, NomAlumne,Cicle,Curs,Grup)
        cur.execute(query,values)
    
        #Confirma la inserción
        conn.commit()
        #Obtiene el último id insertado
        insert_id = cur.lastrowid
    
    except Exception as e:
        return {"status": -1, "message": f"Error de connexió:{e}" }
    
    finally:
        conn.close()

    return insert_id

#Función que comprueba si idAula existe en la tabla "aula"
def aula_existeix(idAula):
    try:
        conn = db_client()
        cur = conn.cursor()
        
        #Consulta SQL para verificar si existe el aula con el id dado
        query = "select count(*) from aula where idAula = %s"
        cur.execute(query,(idAula,))
        
        result = cur.fetchone()
        
    except Exception as e:
        return {"status": -1, "message": f"Error de connexió: {e}"}
    
    finally:
        conn.close()
    
    return result[0]>0

#Función que actualiza el id del alumno pasándole el nuevo id y el nombre del alumno
def update_alumne(idAlumne, idAula, NomAlumne,Cicle,Curs,Grup):
    try:
        conn = db_client()
        cur = conn.cursor()
        
        #Consulta SQL para actualizar todos los campos del alumno según el id
        query = "update alumne SET idAula = %s, NomAlumne = %s, Cicle = %s, Curs = %s, Grup = %s, UpdatedAt = NOW() WHERE idAlumne = %s;"
        values=(idAula, NomAlumne,Cicle,Curs,Grup, idAlumne)
        cur.execute(query,values)
        
        #Número de filas afectadas por la actualización
        updated_alumne = cur.rowcount
        
        #Confirma la actualización
        conn.commit()
    
    except Exception as e:
        return {"status": -1, "message": f"Error de connexió:{e}" }
    
    finally:
        conn.close()

    return updated_alumne

#Función que elimina un alumno pasándole la id
def delete_alumne(id):
    try:
        conn = db_client()
        cur = conn.cursor()
        
        #Consulta SQL para eliminar un alumno según su id
        query = "DELETE FROM alumne WHERE idAlumne = %s;"
        cur.execute(query,(id,))
        
        #Número de filas afectadas por la eliminación
        deleted_alumne = cur.rowcount
        
        #Confirma la eliminación
        conn.commit()
    
    except Exception as e:
        return {"status": -1, "message": f"Error de connexió:{e}" }
    
    finally:
        conn.close()
        
    return deleted_alumne

def insertar_aula(DescAula: str, Edifici: str, Pis: str):
    try:
        conn = db_client()
        cur = conn.cursor()
        
        query = "SELECT * FROM aula WHERE DescAula = %s;"
        cur.execute(query,DescAula)
        aula_existeix = cur.fetchone()
        
        if aula_existeix:
            print(f"L'aula amb DescAula {DescAula} ja existeix.")
        else:
            query_insert_aula= """
            INSERT INTO aula (DescAula, Edifici, Pis, CreatedAt, UpdatedAt)
            VALUES (%s,%s,%s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
            """
        cur.execute(query_insert_aula, (DescAula, Edifici, Pis))
        conn.commit()
        print(f"Aula {DescAula} afegida correctament")
    except Exception as e:
        print(f"Error al afegir aula {e}")
    
    finally:
        conn.close()

def insertar_alumne(NomAlumne: str, Cicle: str, Curs: int, Grup: str, idAula: int):
    try:
        conn = db_client()
        cur = conn.cursor()
        
        query = """
            SELECT * FROM alumne
            WHERE NomAlumne = %s and Cicle = %s and Curs = %s and Grup = %s;
        """
        cur.execute(query, (NomAlumne, Cicle, Curs, Grup))
        alumne_existeix = cur.fetchone()
        
        if alumne_existeix:
            print(f"L'alumne {NomAlumne} ja existeix en el Cicle {Cicle}, Curs {Curs}, Grup {Grup}.")
        else:
            query_insert_alumne = """
                INSERT INTO alumne (NomAlumne, Cicle, Curs, Grup, idAula, CreatedAt, UpdatedAt)
                VALUES (%s,%s,%s,%s,%s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
            """
            cur.execute(query_insert_alumne, (NomAlumne, Cicle, Curs, Grup, idAula))
            conn.commit()
            print(f"Alumne {NomAlumne} inserit correctament.")
    except Exception as e:
        print(f"Error en afegir alumne {e}")
    
    finally:
        conn.close()