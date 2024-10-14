import mysql.connector

#Función que establece la conexión con la base de datos
def db_client():
    
    try:
        #Parámetros de la conexión
        dbname = "alumnes"
        user = "root"
        password = "1234"
        host = "127.0.0.1"
        port = "3306"
        collation = "utf8mb4_general_ci"
        
        #Conexión a la bbdd utilizando mysql.connector
        return mysql.connector.connect(
            host = host,
            port = port,
            user = user,
            password = password,
            database = dbname,
            collation = collation
        ) 
            
    except Exception as e:
        #Si ocurre un error durante la conexión devuelve un mensaje
        return {"status": -1, "message": f"Error de connexió:{e}" }
    