import logging

# API A LA CUAL CONTACTAR DESDE EL WORKER
API_URL = "http://flask/build/"

# DIRECTORIO EN EL HOST DOCKER DONDE GUARDAR LOS BUILDS TEMPORALES
HOME_DIR = "/home/matias/distri2/worker/builds"

# NIVEL DE LOGGING
LOGGING_LEVEL = logging.INFO

# USUARIO Y PASSWORD DEL USUARIO POR DEFECTO
WORKER_USER = 'worker'
WORKER_PASS = 'qpzmalgd'