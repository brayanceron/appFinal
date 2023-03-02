from django.shortcuts import render
import requests


#SERVER_URL="http://192.168.1.57:8000"
SERVER_URL="http://localhost:8000"
def home(request):
    resp = requests.get(SERVER_URL+'/api/getCatalogoTutorias/')   
    #print("FRONT*****"+str(resp.text)) 
    json_response=resp.json()
    
    return render(request,'home.html',{"json_response":json_response})


def getTutoria(request):
    id_tutoria='63e9bc8d811ef54a3de5952c'

    resp = requests.post(SERVER_URL+'/api/getTutoria/',json={'id_tutoria':id_tutoria})   
    json_response=resp.json()

    #print("***** FRONT *****"+str(json_response))
    
    return render(request,'getTutoria.html',{"json_response":json_response})











##METODOS DE LA RESPUESTA
#print(resp)
#print("***** FRONT *****"+str(resp))
#print("***** FRONT *****"+str(resp.json()))
#print("***** FRONT *****"+str(resp.status_code))
#print("***** FRONT *****"+str(resp.text))
#print("***** FRONT *****"+str(resp.content))

#ACCEDER A LA INFORMACION(JSON) DE LA RESPUESTA
#print("***** FRONT ***** "+str(json_response[0]['nombre']))