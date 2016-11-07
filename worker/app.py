from docker import Client

import beanstalkc
import os
import requests

import json

API_URL = "http://flask/build/"


beanstalk = beanstalkc.Connection(host='beanstalk', port=11300)
dock = Client(base_url="unix://var/run/docker.sock", version='auto')


def new_container(config):
	if len(dock.containers(all=True, filters={"name":"build_00"})) > 0:
		dock.remove_container( "build_00" )

	if config == "python:2.7":
		return dock.create_container(image="python:2.7", command='/bin/bash -c "cd /appbuild; pip install pytest; pytest" ', volumes="/appbuild", name="build_00", host_config = dock.create_host_config(binds={"/home/matias/distri2/worker/build":{'bind':'/appbuild', 'mode':'rw'}}))

	return None


def make_build(bid, path):
	if os.path.exists(os.path.join(os.getcwd(), "build")):
		os.system("rm -r build")

	print("[1] Clonando repositorio")
	os.system("git clone " + path + " build")
	#os.system("git clone https://github.com/mat105/GITPYTHONTESTS.git build")
	print("[2] Creando contenedor")
	#ret = dock.create_container(image="python:2.7", command='/bin/bash -c "ls; cd /appbuild; pip install pytest; pytest" ', volumes="/appbuild", name="build_00", host_config = dock.create_host_config(binds={"/home/matias/distri2/worker/build":{'bind':'/appbuild', 'mode':'rw'}}))
	
	ncontainer = new_container("python:2.7")

	if ncontainer:
		res = dock.start( ncontainer['Id'] )
	
		print("[3] Ejecutando tests")
		dock.wait(ncontainer['Id'])
		outpt = dock.logs(ncontainer['Id'])

		fout = str(outpt)
		fout = fout.replace('\\n', '\n')
		fout = fout.replace('\\t', '\t')

		print(fout)
		
		req = requests.put(API_URL+str(bid), data={'output':fout})

		if req.status_code == 200:
			print("[4] Datos guardados")
		else:
			print("[4] Error: Imposible contactar a la API")

		print("[5] Parando contenedor")

		dock.stop( ncontainer['Id'] )

		print("[6] Destruyendo contenedor")
		dock.remove_container( ncontainer['Id'] )
	else:
		print("El lenguaje especificado no es soportado")

	if os.path.exists(os.path.join(os.getcwd(), "build")):
		os.system("rm -r build")



while True:
	job = beanstalk.reserve()
	print(job.body)
	jobdata = json.loads(job.body)
	make_build(jobdata['id'], jobdata['path'])
	job.delete()

