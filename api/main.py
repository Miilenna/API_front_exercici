from fastapi import FastAPI,HTTPException

from pydantic import BaseModel

from typing import List

from fastapi.middleware.cors import CORSMiddleware

import alumnes
import db_alumnes

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Modelo pydantic para representar un alumno
class alumne(BaseModel):
    idAula: int
    NomAlumne: str
    Cicle: str
    Curs: int
    Grup: str

class tablaAlumne(BaseModel):
    NomAlumne: str
    Cicle: str
    Curs: int
    Grup: str
    DescAula: str
    
#Modelo pydantic para representar un aula
class aula(BaseModel):
    DescAula: str
    Edifici: str
    Pis: str

# ------------------------------- PETICIÓN GET -------------------------------

#Endpoint básico
@app.get("/")
def read_root():
    return {"Alumnes API"}

#Endpoint para mostrar todos los alumnos
@app.get("/alumne/list", response_model=List[tablaAlumne])
def read_alumne():
    alumnes_list = alumnes.alumnes_schema(db_alumnes.read_alumne())
    print("Alumnes List:", alumnes_list)  # Imprime la lista de alumnos en la terminal
    return alumnes_list
    #Lee todos los alumnos de la base de datos y los devuelve
    #return alumnes.alumnes_schema(db_alumnes.read_alumne())

#Endpoint para mostrar un alumno en función de su id
@app.get("/alumne/show/{idAlumne}", response_model=dict)
def read_alumnes_id(idAlumne: int):
    #Busca un alumno por su id en la bbdd
    result = db_alumnes.read_id(idAlumne)
    if result is not None:
        #Si lo encuentra lo devuelve
        alum = alumnes.alumne_schema(result)
    else:
        #Si no lo encuentra muestra un mensaje de que no se ha encontrado
        raise HTTPException(status_code=404, detail="Alumne per mostrar no trobat")
    return alum

#Endpoint para mostrar todos los alumnos y todas las aulas
@app.get("/alumne/listAll", response_model=List[dict])
def read_all():
    try:
        #Lee todos los alumnos y aulas que hay
        alumnes_list = alumnes.alumnes_schema(db_alumnes.read_alumne())
        aules_list = alumnes.aules_schema(db_alumnes.readAula())
        
        #Devuelve los alumnos y aulas
        return [{"alumnes" : alumnes_list, "aules":aules_list}]
    
    except Exception as e: 
        #Si ocurre algún error, devuelve que error ha sido
        return {"status": -1, "msg": f"Error ocurred: {e}"}
    
# ------------------------------- PETICIÓN POST -------------------------------

#Endpoint para añadir un nuevo alumno
@app.post("/alumne/add")
async def create_alumne(data: alumne):
    #Extrae la información del nuevo alumno
    idAula = data.idAula
    NomAlumne = data.NomAlumne
    Cicle = data.Cicle
    Curs = data.Curs
    Grup = data.Grup
    
    #Verificar si el idAula existe
    aula_existeix = db_alumnes.aula_existeix(idAula)
    
    if not aula_existeix:
        raise HTTPException(status_code=404, detail="El idAula no existeix")
    
    #Si el idAula existe, agrega al alumno en la base de datos
    l_alumne_id = db_alumnes.create_alumne(idAula,NomAlumne,Cicle,Curs,Grup)
    
    #Devuelve un mensaje de que se ha creado correctamente junto al id y el nombre del alumno
    return {
        "msg": "S'ha afegit correctement"
    }
    
# ------------------------------- PETICIÓN PUT -------------------------------    
    
#Endpoint para actualizar los campos del alumno según la id
@app.put("/alumne/update/{idAlumne}")
def update_alumne(idAlumne: int, idAula: int, NomAlumne:str,Cicle:str,Curs:int,Grup:str):
    
    #Verificar si el idAula existe
    aula_existeix = db_alumnes.aula_existeix(idAula)
    
    if not aula_existeix:
        raise HTTPException(status_code=404, detail="El idAula no existeix")
    
    #Si el aula existe actualiza los campos del alumno en la base de datos
    updated_alumne = db_alumnes.update_alumne(idAlumne, idAula, NomAlumne,Cicle,Curs,Grup)
    
    #Si se ha actualizado correctamente
    if (updated_alumne):
        return {
            "msg": "S'ha modificat correctement"
        }
    #Si no encuentra al alumno para actualizar
    if updated_alumne == 0:
       raise HTTPException(status_code=404, detail="Alumne per actualitzar no trobat") 

# ------------------------------- PETICIÓN DELETE -------------------------------

#Endpoint para eliminar a un alumno por su id
@app.delete("/alumne/delete/{idAlumne}")
def delete_alumne(idAlumne:int):
    
    #Llama a la función para eliminar al alumno de la base de datos
    deleted_alumne = db_alumnes.delete_alumne(idAlumne)
    
    #Si se ha eliminado correctamente
    if (deleted_alumne):
        return {
            "msg": "S'ha esborrat correctament"
        }
    # Si no encuentra al alumno para eliminar
    if deleted_alumne == 0:
       raise HTTPException(status_code=404, detail="Alumne per eliminar no trobat")
