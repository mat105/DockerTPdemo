from docker import Client

import beanstalkc
import os
import requests
import logging

import json
import sys

API_URL = "http://flask/build/"

HOME_DIR = "/home/matias/distri2/worker/build"

LOGGING_LEVEL = logging.INFO


logging.basicConfig(level=logging.INFO)

handler = logging.FileHandler('logs/output.log')
handler.setLevel(logging.INFO)

handlerconsole = logging.StreamHandler(stream=sys.stdout)
handlerconsole.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

beanstalk = beanstalkc.Connection(host='beanstalk', port=11300)
dock = Client(base_url="unix://var/run/docker.sock", version='auto')


class Logger:
	logger = None

	@staticmethod
	def get():
		if Logger.logger == None:
			Logger.logger = logging.getLogger(__name__)
			Logger.logger.setLevel(LOGGING_LEVEL)
			Logger.logger.addHandler(handler)
			Logger.logger.addHandler(handlerconsole)

		return Logger.logger



class Language:
	commands = {}

	@staticmethod
	def get(name):
		return Language.commands.get(name, None)

	def __init__(self, name, image, command):
		self.image = image
		self.command = command

		Language.commands[name] = self

		
def create_languages():
	Language("python", "python:2.7", '/bin/bash -c "cd /appbuild; pip install pytest; pytest" ')
	Language("java", "maven:latest", '/bin/bash -c "ls;cd /appbuild;ls; mvn clean install; mvn test; ls" ')
		



def new_container(config, logger):
	if len(dock.containers(all=True, filters={"name":"build_00"})) > 0:
		logger.info('Borrando contenedor preexistente')
		dock.remove_container( "build_00" )

	ret = Language.get(config)

	if ret != None: #config == "python":
		logger.info('Creando contenedor')
		ret = dock.create_container(image=ret.image, command=ret.command, volumes="/appbuild", name="build_00", host_config = dock.create_host_config(binds={HOME_DIR:{'bind':'/appbuild', 'mode':'rw'}}))
		#ret = dock.create_container(image=ret["image"], command=ret["command"], volumes="/appbuild", name="build_00", host_config = dock.create_host_config(binds={"/home/matias/distri2/worker/build":{'bind':'/appbuild', 'mode':'rw'}}))


	return ret



def make_build(bid, path):
	logger = Logger.get()
	ncontainer = None
	noconf = False

	if os.path.exists(os.path.join(os.getcwd(), "build")):
		os.system("rm -r build")

	logger.info('[0] Iniciando build N# %d' % (bid,))
	logger.info('[1] Clonando repositorio %s' % (path,) )
	os.system("git clone " + path + " build")
	logger.info('[2] Creando contenedor')

	try:
		conf_file = open("build/confTest.json")
	except IOError:
		noconf=True
	else:
		with conf_file:
			jdata = json.load(conf_file)

			ncontainer = new_container(jdata["language"], logger)


	if ncontainer != None and noconf == False:
		res = dock.start( ncontainer['Id'] )
	
		logger.info("[3] Ejecutando tests")

		dock.wait(ncontainer['Id'])
		outpt = dock.logs(ncontainer['Id'])

		fout = str(outpt)
		fout = fout.replace('\\n', '\n')
		fout = fout.replace('\\t', '\t')

		print(fout)
		
		req = requests.put(API_URL+str(bid), data={'output':fout}, auth=('worker', 'qpzmalgd'))

		if req.status_code == 200:
			logger.info("[4] Datos guardados")
		else:
			print(req.status_code)
			logger.error("[4] Imposible contactar a la API")

		logger.info("[5] Parando contenedor")

		dock.stop( ncontainer['Id'] )

		logger.info("[6] Destruyendo contenedor")
		dock.remove_container( ncontainer['Id'] )
	elif noconf:
		logger.error('[3] Archivo de configuracion inexistente')
	else:
		logger.error("[3] El lenguaje especificado no es soportado")

	if os.path.exists(os.path.join(os.getcwd(), "build")):
		os.system("rm -r build")

	logger.info("[x] Terminando\n")



create_languages()


while True:
	job = beanstalk.reserve()
	jobdata = json.loads(job.body)
	make_build(jobdata['id'], jobdata['path'])
	job.delete()


