//alert("ok")


fetch('http://localhost:8000/getCatalogoTutorias/')
  .then(response => response.json())
  .then(data => console.log(data));