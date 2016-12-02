# tp_distribuida2

Testeador

Un pequeño sistema de tests a través de la red.

Rutas:
/build [GET]
> Parametros: {order=(path|date|finished), list=(asc|desc), path=nombreFiltro, finished=(true|false)}
> Trae todos los builds del usuario segun los filtros brindados.

/build [POST]
> Parametros: path = repositorio, {slack=hook de slack para notificar}
> Ordena un nuevo test al repositorio del parametro path, al terminar notifica al hook de slack si este es brindado.

/build/(ID) [GET]
> Trae información respecto al build ID.


Requisitos:

- docker
- docker-compose
- Modifique HOME_DIR en la config del worker por la ruta a su carpeta del worker en el sistema y sumele /builds

Comandos:

- docker-compose up -d
- docker-compose scale beanwork=[NUMERO DE WORKERS A LANZAR]

Primera vez que corre los contenedores:
- docker exec {contenedor_flask_nombre} /bin/bash -c "python /app/dbmake.py"

Probando:
- docker ps; post request a /build con parametro path=repositorioGIT; docker logs {NOMBRE_CONTENEDOR_BEANWORK};

Lenguajes soportados:
- Python 2.7
- Java con maven
