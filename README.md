# tp_distribuida2

Testeador

Requisitos:

- docker
- docker-compose

Comandos:

- docker-compose up -d
- docker-compose scale beanwork=[NUMERO DE WORKERS A LANZAR]

Primera vez:
- docker exec {contenedor_flask_nombre} /bin/bash -c "python /app/dbmake.py"
- docker pull python:2.7
- docker pull maven

Probando:
- docker ps; docker logs {NOMBRE_CONTENEDOR_BEANWORK}

Lenguajes soportados:
- Python 2.7
- Java con maven
