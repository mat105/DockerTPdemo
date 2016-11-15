from docker import Client

import beanstalkc
import os
import requests
import logging

import json

API_URL = "http://flask/build/"

LOGGING_LEVEL = logging.INFO


logging.basicConfig(level=logging.INFO)

handler = logging.FileHandler('logs/output.log')
handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

beanstalk = beanstalkc.Connection(host='beanstalk', port=11300)
dock = Client(base_url="unix://var/run/docker.sock", version='auto')


class Logger:
	@@logger = None

	def get():
		if @@logger == None:
			@@logger = logging.getLogger(__name__)
			@@logger.setLevel(LOGGING_LEVEL)
			@@logger.addHandler(handler)

		return @@logger


def new_container(config, logger):
	if len(dock.containers(all=True, filters={"name":"build_00"})) > 0:
		logger.info('Borrando contenedor preexistente')
		dock.remove_container( "build_00" )

	if config == "python":
		logger.info('Creando contenedor')
		return dock.create_container(image="python:2.7", command='/bin/bash -c "cd /appbuild; pip install pytest; pytest" ', volumes="/appbuild", name="build_00", host_config = dock.create_host_config(binds={"/home/matias/distri2/worker/build":{'bind':'/appbuild', 'mode':'rw'}}))

	return None


def make_build(bid, path):
	logger = Logger.get()
	ncontainer = None
	noconf = False

	if os.path.exists(os.path.join(os.getcwd(), "build")):
		os.system("rm -r build")

	logger.info('[1] Clonando repositorio"')
	print("[1] Clonando repositorio")
	os.system("git clone " + path + " build")
	logger.info('[2] Creando contenedor"')
	print("[2] Creando contenedor")

	try:
		conf_file = open("confTest.json")
	except IOError:
		noconf=True
	else:
		with conf_file:
			jdata = json.load(conf_file)

			ncontainer = new_container(jdata["language"], logger)


	if ncontainer != None and noconf == False:
		res = dock.start( ncontainer['Id'] )
	
		logger.info("[3] Ejecutando tests")
		print("[3] Ejecutando tests")

		dock.wait(ncontainer['Id'])
		outpt = dock.logs(ncontainer['Id'])

		fout = str(outpt)
		fout = fout.replace('\\n', '\n')
		fout = fout.replace('\\t', '\t')

		print(fout)
		
		req = requests.put(API_URL+str(bid), data={'output':fout}, auth=('worker', '123'))

		if req.status_code == 200:
			logger.info("[4] Datos guardados")
			print("[4] Datos guardados")
		else:
			logger.error("[4] Imposible contactar a la API")
			print("[4] Error: Imposible contactar a la API")

		logger.info("[5] Parando contenedor")
		print("[5] Parando contenedor")

		dock.stop( ncontainer['Id'] )

		logger.info("[6] Destruyendo contenedor")
		print("[6] Destruyendo contenedor")
		dock.remove_container( ncontainer['Id'] )
	elif noconf:
		logger.error('[3] Archivo de configuracion inexistente')
		print('[3] Archivo de configuracion inexistente')
	else:
		logger.error("[3] El lenguaje especificado no es soportado")
		print("[3] El lenguaje especificado no es soportado")

	if os.path.exists(os.path.join(os.getcwd(), "build")):
		os.system("rm -r build")


while True:
	job = beanstalk.reserve()
	jobdata = json.loads(job.body)
	make_build(jobdata['id'], jobdata['path'])
	job.delete()
