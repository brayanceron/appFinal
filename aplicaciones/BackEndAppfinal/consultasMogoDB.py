from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.json_util import dumps
from datetime import datetime


client = MongoClient()
client = MongoClient('localhost', 27017)

db = client.BDAPPFINAL
collection = db.tutorias

def getIdUsuarioMongo(correo):
    result=db.usuarios.find_one({"correo":correo});
    id=str(result["_id"])
    
    return id

def getInfoUsuarioMongo(correo):
    result=db.usuarios.find({"correo":correo});
    print(result)
    list_cur = list(result)
    print(list_cur)
    
    json_string_data = dumps(list_cur)#convirtiendo a json el diccionario anterior
    print(json_string_data)
    return json_string_data



def getMisTutoriasEnProgresoEstudianteMongo(id_usuario):
    pipeline = [
    {"$match":{"id_estudiantes":ObjectId(id_usuario)}},
    #{"$lookup": {"from":"profesores","localField":"id_profesor","foreignField":"_id","as":"id_profesor"}}, SIN UNIFICAR
    {"$lookup": {"from":"usuarios","localField":"id_profesor","foreignField":"_id","as":"id_profesor"}},
    ]
    results=collection.aggregate(pipeline)
    list_cur = list(results)#convirtiendo a diccionario el resultado
    json_string_data = dumps(list_cur)#convirtiendo a json el diccionario anterior
    return json_string_data #se devuelve una cadena en formato json


def getMisTutoriasEnProgresoProfesorMongo(id_usuario):
    pipeline = [
    {"$match":{"id_profesor":ObjectId(id_usuario)}},
    #{"$lookup": {"from":"profesores","localField":"id_profesor","foreignField":"_id","as":"id_profesor"}}, SIN UNIFICAR
    {"$lookup": {"from":"usuarios","localField":"id_profesor","foreignField":"_id","as":"id_profesor"}},
    ]
    results=collection.aggregate(pipeline)
    list_cur = list(results)#convirtiendo a diccionario el resultado
    json_string_data = dumps(list_cur)#convirtiendo a json el diccionario anterior
    return json_string_data 


def getSolicitudesProfesorMongo(id_usuario):
    pipeline = [
    {"$match":{"id_profesor":ObjectId(id_usuario)}},
    {"$match":{"estado":"ESPERA"}},
    {"$lookup":{"from":"tutoriasPublicadas","localField":"id_tutoria_publicada","foreignField":"_id","as":"id_tutoria_publicada"}},
    {"$lookup":{"from":"usuarios","localField":"id_solicitante","foreignField":"_id","as":"id_solicitante"}},
    {"$lookup":{"from":"usuarios","localField":"id_profesor","foreignField":"_id","as":"id_profesor"}}
    ]
    results=db.solicitudes.aggregate(pipeline)
    list_cur = list(results)#convirtiendo a diccionario el resultado
    json_string_data = dumps(list_cur)#convirtiendo a json el diccionario anterior
    return json_string_data


def getSolicitudesEstudianteMongo(id_usuario):
    pipeline = [
    {"$match":{"id_solicitante":ObjectId(id_usuario)}}, #Esto debe estar activo, esta desabilitado solamente para pruebas
    {"$lookup":{"from":"tutoriasPublicadas","localField":"id_tutoria_publicada","foreignField":"_id","as":"id_tutoria_publicada"}},
    {"$lookup":{"from":"usuarios","localField":"id_solicitante","foreignField":"_id","as":"id_solicitante"}},
    {"$lookup":{"from":"usuarios","localField":"id_profesor","foreignField":"_id","as":"id_profesor"}}
    ]
    results=db.solicitudes.aggregate(pipeline)
    list_cur = list(results)#convirtiendo a diccionario el resultado
    json_string_data = dumps(list_cur)#convirtiendo a json el diccionario anterior
    return json_string_data


def getMisTutoriasPublicadasMongo(id_usuario):
    pipeline = [
    {"$match":{"id_profesor":ObjectId(id_usuario)}},
    {"$lookup": {"from":"usuarios","localField":"id_profesor","foreignField":"_id","as":"id_profesor"}},
    ]
    results=db.tutoriasPublicadas.aggregate(pipeline)
    list_cur = list(results)#convirtiendo a diccionario el resultado
    json_string_data = dumps(list_cur)#convirtiendo a json el diccionario anterior
    return json_string_data #se devuelve una cadena en formato json


def getTutoriaMongo(id_tutoria):
    
    pipeline = [
    {"$match": {"_id": ObjectId(id_tutoria)}},
    #{"$lookup": {"from":"profesores","localField":"id_profesor","foreignField":"_id","as":"id_profesor"}}, SIN UNIFICAR
    {"$lookup": {"from":"usuarios","localField":"id_profesor","foreignField":"_id","as":"id_profesor"}},
    #{"$lookup": {"from":"estudiantes","localField":"id_estudiantes","foreignField":"_id","as":"id_estudiantes"}}, SIN UNIFICAR
    {"$lookup": {"from":"usuarios","localField":"id_estudiantes","foreignField":"_id","as":"id_estudiantes"}},
    ]
    
    results=collection.aggregate(pipeline)
    list_cur = list(results)
    

    
    json_string_data = dumps(list_cur)#convirtiendo a json el diccionario anterior
    return json_string_data #se devuelve una cadena en formato json


def getCatalogoTutoriasMongo():
    pipeline = [
    {"$lookup": {"from":"usuarios","localField":"id_profesor","foreignField":"_id","as":"id_profesor"}},
    {"$lookup": {"from":"usuarios","localField":"id_estudiantes","foreignField":"_id","as":"id_estudiantes"}},
    ]
    
 
    results=db.tutoriasPublicadas.aggregate(pipeline)
    list_cur = list(results)
    
    json_string_data = dumps(list_cur)#convirtiendo a json el diccionario anterior
    #print("BACK*****"+ str(json_string_data))
    return json_string_data #se devuelve una cadena en formato json


def publicarTutoriaMongo(json_data):
    print(json_data)
    print(type(json_data))

    
    save={
            "nombre":json_data[0],
            "id_profesor":ObjectId(json_data[1]),
            #"id_estudiantes":[],
            "estado":"Activo",
            "descripcion":json_data[2],
            "calificacion":0,
            #"tipo":"I",
            #"entradas":[]
        }
    print(save)
    
    #results=collection.insert_one(save);
    results=db.tutoriasPublicadas.insert_one(save);



def getContenidoTutoriaMongo(id_tutoria):
    pipeline = [
    {"$match": {"id_tutoria": ObjectId(id_tutoria)}},
    #{"$lookup": {"from":"tutorias","localField":"id_tutoria","foreignField":"_id","as":"id_tutoria"}},
    
    
    #{"$lookup": {"from":"profesores","localField":"id_profesor","foreignField":"_id","as":"id_profesor"}}, SIN UNIFICAR
    {"$lookup": {"from":"usuarios","localField":"id_profesor","foreignField":"_id","as":"id_profesor"}},
    ]
    
    results=db.entradasTutorias.aggregate(pipeline)
    list_cur = list(results)
    

    
    json_string_data = dumps(list_cur)#convirtiendo a json el diccionario anterior
    return json_string_data #se devuelve una cadena en formato json

def getEntradaMongo(id_tutoria):
    pipeline = [
    {"$match": {"_id": ObjectId(id_tutoria)}},
    {"$lookup": {"from":"profesores","localField":"id_profesor","foreignField":"_id","as":"id_profesor"}},
    ]
    
    results=db.entradasTutorias.aggregate(pipeline)
    list_cur = list(results)
    
    json_string_data = dumps(list_cur)#convirtiendo a json el diccionario anterior
    return json_string_data #se devuelve una cadena en formato json



def registrarEntradaMongo(data): #data es un vector de 4 pociciones que contiene [id_tutoria,id_profesor,titulo,descripcion]
    print(data)
    print(type(data))
    now = datetime.now()
    fecha_creacion= str(now.day)+"/"+str(now.month)+"/"+str(now.year)+"   "+str(now.hour)+":"+str(now.minute)
    
    save={            
            "id_tutoria":ObjectId(data[0]),
            "id_profesor":ObjectId(data[1]),
            "titulo":data[2],
            "descripcion":data[3],
            "fecha_creacion":fecha_creacion,
            "archivos":[],
        }
    print(save)
    
    #results=db.entradasTutorias.insert_one(save)
    insesrcion=db.entradasTutorias.insert_one(save)
    
    
    id_insesrcion=insesrcion.inserted_id
    #print ("id insertado: "+str(id_insesrcion))
    collection.update_one(
    {"_id": ObjectId(data[0])   },
    {"$addToSet":{"entradas":  ObjectId(id_insesrcion) }}
    )
    

def updateEntradaMongo(data):
    print(data)
    print(type(data))
    now = datetime.now()
    fecha_creacion= str(now.day)+"/"+str(now.month)+"/"+str(now.year)+"   "+str(now.hour)+":"+str(now.minute)
    
    id_entrada=data[0]
    titulo=data[1]
    descripcion=data[2]
    
    #results=db.entradasTutorias.insert_one(save)
    db.entradasTutorias.update_one(
        {"_id": ObjectId(id_entrada)},
        {"$set":{"titulo":titulo,"descripcion":descripcion,"fecha_creacion":fecha_creacion}}
        )
    
 
def rechazarSolicitudMongo(id_solicitud,id_usuario):
    #obteniendo el id del profesor dueño de la tutoria en la base de datos
    
    #res=db.solicitudes.find_one({"id_profesor":ObjectId(id_usuario)},{"_id":0,"id_profesor":1})
    res=db.solicitudes.find_one({"_id":ObjectId(id_solicitud)},{"_id":0,"id_profesor":1})
    
    print("Verdadero propietario tutoria(profesor): "+str(res["id_profesor"]))
    print("Propietario recivido: "+id_usuario)
    
    if(str(res["id_profesor"])==str(id_usuario)): #se valida que es el dueño de la tutoria
        try:
            db.solicitudes.update_one(
                {"_id": ObjectId(id_solicitud)},
                {"$set":{"estado":"RECHAZADA"}}
            )
            return "200"
        except:
            return "500"
        
    else:
        return "403"
    

def cancelarSolicitudMongo(id_solicitud,id_usuario):
    #obteniendo el id del profesor dueño de la tutoria en la base de datos
    res=db.solicitudes.find_one({"id_solicitante":ObjectId(id_usuario)},{"_id":0,"id_solicitante":1})
    
    print("Verdadero propietario solicitud(estudiante): "+str(res["id_solicitante"]))
    print("Propietario recivido: "+id_usuario)
    
    if(str(res["id_solicitante"])==str(id_usuario)): 
        try:
            db.solicitudes.update_one(
                {"_id": ObjectId(id_solicitud)},
                {"$set":{"estado":"CANCELADA"}}
            )
            return "200"
        except:
            return "500"
        
    else:
        return "403"
   

def registrarSolicitudMongo(id_tutoria_publicada,id_solicitante,id_profesor):
    save={
            "id_tutoria_publicada":ObjectId(id_tutoria_publicada),
            "id_solicitante":ObjectId(id_solicitante),
            "id_profesor":ObjectId(id_profesor),
            "estado":"ESPERA"
        }
    print(save)
    
    #results=db.solicitudes.insert_one(save);
    
    try:
        results=db.solicitudes.insert_one(save);
        return "200"
    except:
        return "500"



def aceptarSolicitudMongo(id_solicitud,id_usuario):
    #obteniendo el id del profesor dueño de la tutoria en la base de datos
    
    #res=db.solicitudes.find_one({"id_profesor":ObjectId(id_usuario)},{"_id":0,"id_profesor":1})
    res=db.solicitudes.find_one({"_id":ObjectId(id_solicitud)},{"_id":0,"id_profesor":1})
    
    print("Verdadero propietario tutoria(profesor): "+str(res["id_profesor"]))
    print("Propietario recivido: "+id_usuario)
    
    if(str(res["id_profesor"])==str(id_usuario)): #se valida que es el dueño de la tutoria
        try:
            db.solicitudes.update_one(
                {"_id": ObjectId(id_solicitud)},
                {"$set":{"estado":"ACEPTADA"}}
            );
            
            #Aqui se crea la instancia de la tutoriaPublicada, producto de aceptar la solicitud
            st=crearInstanciaTutoriaPublicada(id_solicitud,id_usuario);
            
            return st;
        except Exception as err:
            #print(str(err))
            return "500"
        
    else:
        return "403"


def crearInstanciaTutoriaPublicada(id_solicitud,id_usuario):
    pipeline = [
    {"$match": {"_id": ObjectId(id_solicitud)}},
    {"$lookup": {"from":"tutoriasPublicadas","localField":"id_tutoria_publicada","foreignField":"_id","as":"id_tutoria_publicada"}},
    {"$lookup": {"from":"usuarios","localField":"id_solicitante","foreignField":"_id","as":"id_solicitante"}},
    {"$lookup": {"from":"usuarios","localField":"id_profesor","foreignField":"_id","as":"id_profesor"}},
    ]

    res=db.solicitudes.aggregate(pipeline)
    list_cur = list(res)
    print(str(list_cur))
    
    if(id_usuario==str(list_cur[0]["id_profesor"][0]["_id"])):#validando que el usuario que envio la peticion desde el front sea el dueño de la tutoria
        save={
        "_id_tutoria_publicada":list_cur[0]["id_tutoria_publicada"][0]["_id"],
        "nombre":list_cur[0]["id_tutoria_publicada"][0]["nombre"]+"("+list_cur[0]["id_solicitante"][0]["nombre"]+")",
        #"id_profesor":ObjectId(id_usuario),
        "id_profesor":list_cur[0]["id_profesor"][0]["_id"],
        "id_estudiantes":[ObjectId(list_cur[0]["id_solicitante"][0]["_id"])],
        "estado":"ACTIVA",
        "descripcion":list_cur[0]["id_tutoria_publicada"][0]["descripcion"],
        "calificacion":0,
        "tipo":"I",
        "entradas":[]
        }
    
        print(str(save))
        
        try:
            insesrcion=db.tutorias.insert_one(save);
            id_insesrcion=insesrcion.inserted_id
            
            #CREANDO LA ENTRADA BIENVENIDA POR DEFECTO
            #data=[id_tutoria,id_profesor,titulo,descripcion]
            titulo="Bienvenida!"
            descripcion='Has iniciado un nuevo camino de aprendizaje,  te damos la bienvenida a la tutoria de "'+list_cur[0]["id_tutoria_publicada"][0]["nombre"]+'"'
            data=[id_insesrcion,list_cur[0]["id_profesor"][0]["_id"],titulo,descripcion]
            try:
                registrarEntradaMongo(data)
                return "200";
            except:
                return "500";
            
        except:
            return "500";
        
        
    
    else:
        return "403";
    
    
def unirmeTutoriaMongo(id_tutoria,id_usuario):
    #buscando si existe la tutoria
    
    try:
        results=db.tutorias.find_one({"_id":ObjectId(id_tutoria)});
        list_cur = list(results)
        print("lalis=> "+str(list_cur))
        
        #aqui la logica para que despues que encontro la tutoria proceda a ingresar el estudiante
        try:
            #VALIDAR QUE UN MISMO USUARIO NO SE VAYA A INSCRIBIR MAS DE UNA MES A LA MISMA TUTORIA OOOOJJJJOOOO AQUI
            db.tutorias.update_one(
            {"_id": ObjectId(id_tutoria)   },
            {"$addToSet":{"id_estudiantes":  ObjectId(id_usuario) }})
            return "200"
        except:
            return "404"   
        #json_string_data = dumps(list_cur)#convirtiendo a json el diccionario anterior
        #print("longitud= "+str(len(list_cur)))
        
        
        
    except:
        return "404"
    






#
#print (json_data)
    
#para mostrar resultados
#for result in results:
#    print(result)
    
    
print("Ok here")