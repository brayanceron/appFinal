from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render
from django.views.generic import View
from django.core.files.storage import FileSystemStorage
from .consultasMogoDB import *
import json




def root(request):
    return HttpResponse("Oki")

@csrf_exempt 
def rutaUno(request):
    
    if request.method == 'GET':
        print("Peticion get recivida")
        return JsonResponse({"prueba_get":"OK","atributo2":"valor 2"})
    
    elif request.method == 'POST':
        print("Peticion post recivida")
        data =json.loads(request.body.decode("utf-8")) 
        print(data)
        print(data["datos_peticion"])
        return JsonResponse({"prueba_post":"OK"})
    
@csrf_exempt 
def getInfoUsuario(request):
    if request.method == 'POST':
        print("Buscando informacion de un usuario")
        datarecivida =json.loads(request.body.decode("utf-8")) 
        correo=datarecivida['correo']
        
        listaR=json.loads(getInfoUsuarioMongo(correo))
        #print(listaR)
        return JsonResponse((listaR),safe=False)




@csrf_exempt 
def getMisTutoriasEnProgresoEstudiante(request):
    datarecivida =json.loads(request.body.decode("utf-8")) 
    
    correo=datarecivida['correo']
    id_usuario=getIdUsuarioMongo(correo)
    
    print("Enviando  tutorias del usuario: "+id_usuario )
    listaR=json.loads(getMisTutoriasEnProgresoEstudianteMongo(id_usuario)) #se convierte a json la cadena que viene en formato json
    return JsonResponse((listaR),safe=False)

@csrf_exempt 
def getMisTutoriasEnProgresoProfesor(request):
    datarecivida =json.loads(request.body.decode("utf-8")) 
    
    correo=datarecivida['correo']
    id_usuario=getIdUsuarioMongo(correo)
    
    print("Enviando  tutorias del usuario: "+id_usuario )
    listaR=json.loads(getMisTutoriasEnProgresoProfesorMongo(id_usuario)) #se convierte a json la cadena que viene en formato json
    return JsonResponse((listaR),safe=False)




@csrf_exempt 
def getMisTutoriasPublicadas(request):
    datarecivida =json.loads(request.body.decode("utf-8")) 
    
    correo=datarecivida['correo']
    id_usuario=getIdUsuarioMongo(correo)
    
    print("Enviando  tutorias del usuario: "+id_usuario )
    listaR=json.loads(getMisTutoriasPublicadasMongo(id_usuario)) #se convierte a json la cadena que viene en formato json
    return JsonResponse((listaR),safe=False)

    
@csrf_exempt 
def getTutoria(request):
    if request.method == 'POST':
        print("Buscando tutoria")
        datarecivida =json.loads(request.body.decode("utf-8")) 
        
        id_tutoria=datarecivida['id_tutoria']
        #print("***** BACK *****"+str(id_tutoria))
        listaR=json.loads(getTutoriaMongo(id_tutoria))
        return JsonResponse((listaR),safe=False)
    
@csrf_exempt 
def getCatalogoTutorias(request):
    if request.method == 'GET':
        print("Buscando todas tutoria")
        
        listaR=json.loads(getCatalogoTutoriasMongo())
        return JsonResponse((listaR),safe=False)
    
@csrf_exempt 
def getContenidoTutoria(request):
    if request.method == 'POST':
        print("Buscando Contenido de la tutoria")
        datarecivida =json.loads(request.body.decode("utf-8")) 
        
        id_tutoria=datarecivida['id_tutoria']
        listaR=json.loads(getContenidoTutoriaMongo(id_tutoria))
        print(listaR)
        return JsonResponse((listaR),safe=False)
        
        #return JsonResponse({"ok":"ok"},safe=False)

@csrf_exempt 
def publicarTutoria(request):
    if request.method == 'POST':
        print("registrando tutoria")
        datarecivida =json.loads(request.body.decode("utf-8")) 
        
        nombre=datarecivida['nombre']
        id_profesor=datarecivida['id_profesor']
        descripcion=datarecivida['descripcion']
        
        
        dd=[nombre,id_profesor,descripcion]
        
        print("----------------------------------")
        #print(jsondata)
        #print(type(jsondata))
        #print("----------------------------------")
        publicarTutoriaMongo(dd)
        
        #listaR=json.loads(getTutoriaMongo(id_tutoria))
        return JsonResponse({"ok":"ok"},safe=False)




@csrf_exempt 
def getEntrada(request):
    if request.method == 'POST':
        print("Buscando entrada de la tutoria")
        datarecivida =json.loads(request.body.decode("utf-8")) 
        
        id_entrada=datarecivida['id_entrada']
        print(id_entrada)
        listaR=json.loads(getEntradaMongo(id_entrada))
        print(listaR)
        return JsonResponse((listaR),safe=False)
    
@csrf_exempt 
def registrarEntrada(request):
    if request.method == 'POST':
        print("registrando entrada")
        datarecivida =json.loads(request.body.decode("utf-8")) 
        
        titulo=datarecivida['titulo']
        id_tutoria=datarecivida['id_tutoria']        
        id_profesor=datarecivida['id_profesor']
        descripcion=datarecivida['descripcion']
        
        data=[id_tutoria,id_profesor,titulo,descripcion]

        registrarEntradaMongo(data)
        
        #listaR=json.loads(getTutoriaMongo(id_tutoria))
        return JsonResponse({"ok":"ok"},safe=False)

@csrf_exempt 
def updateEntrada(request):
    if request.method == 'POST':
        print("registrando entrada")
        datarecivida =json.loads(request.body.decode("utf-8")) 
        print("--------------------------------------")
        print("datarecivida: "+str(datarecivida))
        
        titulo=datarecivida['titulo']
        descripcion=datarecivida['descripcion']
        id_entrada=datarecivida['id_entrada']     
        
        
        data=[id_entrada,titulo,descripcion]

        updateEntradaMongo(data)
        
        #listaR=json.loads(getTutoriaMongo(id_tutoria))
        return JsonResponse({"ok":"ok"},safe=False)
    
@csrf_exempt 
def subirArchivotest(request):
    if request.method == 'POST':
        
        myfile=request.FILES['Myarchivo']
        fs= FileSystemStorage()
        filename=fs.save(myfile.name,myfile)
        uploaded_file_url=fs.url(filename)
        print(uploaded_file_url)
        
        print("========================================")
        print(filename)
        print("========================================")
        print("name: "+filename+",size: "+str(myfile.size)+",extension: "+str(myfile.name).split(sep='.')[1])
        print("************")
        return JsonResponse({"ok":"ok"},safe=False)
    
    
@csrf_exempt 
def getSolicitudesProfesor(request):
    if request.method == 'POST':
        datarecivida =json.loads(request.body.decode("utf-8")) 
    
        correo=datarecivida['correo']
        id_usuario=getIdUsuarioMongo(correo)
        
        print("bUSCANDO LAS SOLICITUDES: "+id_usuario )
        listaR=json.loads(getSolicitudesProfesorMongo(id_usuario)) #se convierte a json la cadena que viene en formato json
        return JsonResponse((listaR),safe=False)
    

@csrf_exempt 
def getSolicitudesEstudiante(request):
    if request.method == 'POST':
        datarecivida =json.loads(request.body.decode("utf-8")) 
    
        correo=datarecivida['correo']
        id_usuario=getIdUsuarioMongo(correo)
        
        print("bUSCANDO LAS SOLICITUDES: "+id_usuario )
        listaR=json.loads(getSolicitudesEstudianteMongo(id_usuario)) #se convierte a json la cadena que viene en formato json
        return JsonResponse((listaR),safe=False)

@csrf_exempt 
def rechazarSolicitud(request):
    if request.method == 'POST':
        datarecivida =json.loads(request.body.decode("utf-8")) 
    
        id_solicitud=datarecivida['id_solicitud']
        id_usuario=datarecivida['id_usuario'] #es el id del usuario(debe ser necesariamente un profesor)  que inicio sesion en el front y es el que manda la peticion, se debe validar que sea el dueño de la tutoria
        
        status= rechazarSolicitudMongo(id_solicitud,id_usuario)
        
        print("estado: "+status)
        
        return JsonResponse({},safe=False,status=status)
    

@csrf_exempt 
def cancelarSolicitud(request):
    if request.method == 'POST':
        datarecivida =json.loads(request.body.decode("utf-8")) 
    
        id_solicitud=datarecivida['id_solicitud']
        id_usuario=datarecivida['id_usuario'] #es el id del usuario que inicio sesion en el front y es el que manda la peticion, se debe validar que sea el dueño de la solicitud
        
        status= cancelarSolicitudMongo(id_solicitud,id_usuario)
        
        print("estado: "+status)
        
        return JsonResponse({},safe=False,status=status)
    
@csrf_exempt 
def registrarSolicitud(request):
    if request.method == 'POST':
        datarecivida =json.loads(request.body.decode("utf-8")) 
    
        id_tutoria_publicada=datarecivida['id_tutoria_publicada']
        id_solicitante=datarecivida['id_solicitante']
        id_profesor=datarecivida['id_profesor']
        
        status= registrarSolicitudMongo(id_tutoria_publicada,id_solicitante,id_profesor)
        
        #print("estado: "+status)
        
        return JsonResponse({},safe=False,status=status)
    
@csrf_exempt     
def aceptarSolicitud(request):
    if request.method == 'POST':
        datarecivida =json.loads(request.body.decode("utf-8")) 
    
        id_solicitud=datarecivida['id_solicitud']
        id_usuario=datarecivida['id_usuario'] #es el id del usuario(debe ser necesariamente un profesor) que inicio sesion en el front y es el que manda la peticion, se debe validar que sea el dueño de la tutoria
        
        status= aceptarSolicitudMongo(id_solicitud,id_usuario)
        
        print("estado: "+status)
        
        return JsonResponse({},safe=False,status=status)
    
    
@csrf_exempt    
def unirmeTutoria(request):
    if request.method == 'POST':
        datarecivida =json.loads(request.body.decode("utf-8")) 
    
        id_tutoria=datarecivida['id_tutoria']
        id_usuario=datarecivida['id_usuario'] #es el id del usuario(debe ser necesariamente un profesor) que inicio sesion en el front y es el que manda la peticion, se debe validar que sea el dueño de la tutoria
        
        status= unirmeTutoriaMongo(id_tutoria,id_usuario)
        
        print("estado: "+status)
        
        return JsonResponse({},safe=False,status=status)
    
    