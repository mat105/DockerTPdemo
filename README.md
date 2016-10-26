# tp_distribuida2

Testeador:

Requisitos:

- docker build -t flaskpsyco .
- docker pull postgres

Comandos:

docker run --name postgresdb -e POSTGRES_PASSWORD=123 -p 5432:5432 -d postgres

docker run --name flaskapp --link postgresdb:postgres --restart=always -p 80:80 -v /home/matias/docker-tp:/app -d flaskpsyco

Primera vez:
- GET -> (url)/create # Generar base de datos.

