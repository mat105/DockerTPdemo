# tp_distribuida2

Testeador

Requisitos:

- docker
- docker-compose

Comandos:

- docker-compose up -d

Primera vez:
- docker exec {contenedor_flask_nombre} /bin/bash -c "python /app/dbmake.py"
- docker pull python:2.7
- docker pull maven

Probando:
- GET -> (url)/hola # Envía un pedido de build del repositorio https://github.com/mat105/GITPYTHONTESTS (para probar)
- docker ps; docker logs {NOMBRE_CONTENEDOR_BEANWORK}

Lenguajes soportados:
- Python 2.7
