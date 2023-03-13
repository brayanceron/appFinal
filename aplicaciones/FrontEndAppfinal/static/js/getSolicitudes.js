function aceptarSolicitud(id_solicitud,id_usuario){
    //alert(id_solicitud+"->"+id_usuario)
    const element = document.getElementById(id_solicitud);

    fetch(SERVER_URL+'/api/aceptarSolicitud/',{
      method:'POST',
      body:JSON.stringify({
          "id_solicitud":id_solicitud,
          "id_usuario":id_usuario
      })
    })
    .then(response => response.json())
    .then(data =>{
        id_insercion=data[0].id_insercion.$oid
        //console.log("****** Respuesta front"+data)
        //console.log(data)
        location.href = SERVER_URL+"/web/getContenidoTutoria/"+id_insercion;
        //element.remove();
    } )
    .catch(function(error) {
        console.log('Hubo un problema con la petición Fetch:' + error.message);
    });
}

function rechazarSolicitud(id_solicitud,id_usuario){
    const btnaceptar = document.getElementById("btnaceptar"+id_solicitud);
    const btnrechazar = document.getElementById("btnrechazar"+id_solicitud);
    const lblestado = document.getElementById("lblestado"+id_solicitud);
   
    
    fetch(SERVER_URL+'/api/rechazarSolicitud/',{
      method:'POST',
      body:JSON.stringify({
          "id_solicitud":id_solicitud,
          "id_usuario":id_usuario
      })
    })
    .then(response => response.json())
    .then(data =>{
        console.log(data)
        btnaceptar.remove()
        btnrechazar.remove()
        lblestado.innerText="RECHAZADA"
        
    } )
    .catch(function(error) {
        console.log('Hubo un problema con la petición Fetch:' + error.message);
    });
}

function cancelarSolicitud(id_solicitud,id_usuario){
    const btncancelar = document.getElementById("btncancelar"+id_solicitud);
    const lblcancelar = document.getElementById("lblcancelar"+id_solicitud);
    fetch(SERVER_URL+'/api/cancelarSolicitud/',{
      method:'POST',
      body:JSON.stringify({
          "id_solicitud":id_solicitud,
          "id_usuario":id_usuario
      })
    })
    .then(response => response.json())
    .then(data =>{
        console.log(data)
        //location.href = SERVER_URL+"/web/getSolicitudes/";
        btncancelar.remove();
        lblcancelar.innerText="CANCELADA"
        //element.disabled =true;
    } )
    .catch(function(error) {
        console.log('Hubo un problema con la petición Fetch:' + error.message);
    });
}



function borrarSolicitud(id_solicitud,id_usuario){
    const element = document.getElementById(id_solicitud);
    fetch(SERVER_URL+'/api/borrarSolicitud/',{
      method:'POST',
      body:JSON.stringify({
          "id_solicitud":id_solicitud,
          "id_usuario":id_usuario
      })
    })
    .then(response => response.json())
    .then(data =>{
        console.log(data)
        element.remove();
    } )
    .catch(function(error) {
        console.log('Hubo un problema con la petición Fetch:' + error.message);
    });
}