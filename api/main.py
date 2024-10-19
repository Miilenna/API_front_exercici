from fastapi import FastAPI,HTTPException, Query, File, UploadFile
import csv
import io
from pydantic import BaseModel

from typing import List, Optional

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
def read_alumne(orderby: Optional[str] = None, contain: Optional[str] = None, skip: int = Query(0, ge=0), limit: Optional[int] = Query (100, gt=0)):
    alumnes_list = alumnes.alumnes_schema(db_alumnes.read_alumne())
    
    if not alumnes_list: 
        return []
    
    if contain:
        alumnes_filtrats = []
        contain_lower = contain.lower()
        for alumne in alumnes_list:
            nom_alumne_lower = alumne["NomAlumne"].lower()
            if contain_lower in nom_alumne_lower:
                alumnes_filtrats.append(alumne)
        alumnes_list = alumnes_filtrats
    
    if orderby == "asc":
        alumnes_list = sorted(alumnes_list,key=lambda alumne : alumne["NomAlumne"])
    elif orderby == "desc":
        alumnes_list = sorted(alumnes_list,key=lambda alumne : alumne["NomAlumne"], reverse=True)
    
    alumnes_list = alumnes_list[skip: skip + limit]
    
    return alumnes_list

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

@app.post("/alumne/loadAlumnes")
async def load_alumnes(file: UploadFile = File(...)):
    
    #Si el fichero es .csv
    if file.filename.endswith('.csv'):
        # Lee el fichero .csv
        contents = await file.read()
        
        # de CSV a JSON
        csv_data = io.StringIO(contents.decode('utf-8'))
        csv_reader = csv.DictReader(csv_data)
        json_data = [row for row in csv_reader]
        
        for i in json_data:
            DescAula = i.get("DescAula")
            Edifici = i.get("Edifici")
            Pis = i.get("Pis")
            NomAlumne = i.get("NomAlumne")
            Cicle = i.get("Cicle")
            Curs = int(i.get("Curs"))
            Grup = i.get("Grup")

            idAula = db_alumnes.insertar_aula(DescAula, Edifici, Pis)
            
            db_alumnes.insertar_alumne(NomAlumne, Cicle, Curs, Grup, idAula)
        
        return {
            "resultat": json_data,
            "msg":"Càrrega massiva realitzada correctament"
        }
    
    else:
        return {"error": "Només fichers CSV."}




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
