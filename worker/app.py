from docker import Client

import beanstalkc
import os

beanstalk = beanstalkc.Connection(host='beanstalk', port=11300)
dock = Client(base_url="unix://var/run/docker.sock", version='auto')


def new_container(config):
	if config == "python:2.7":
		return dock.create_container(image="python:2.7", command='/bin/bash -c "cd /appbuild; pip install pytest; pytest" ', volumes="/appbuild", name="build_00", host_config = dock.create_host_config(binds={"/home/matias/distri2/worker/build":{'bind':'/appbuild', 'mode':'rw'}}))

	return None


def make_build(path):
	if os.path.exists(os.path.join(os.getcwd(), "build")):
		os.system("rm -r build")

	print("[1] Clonando repositorio")
	os.system("git clone " + path + " build")
	#os.system("git clone https://github.com/mat105/GITPYTHONTESTS.git build")
	print("[2] Creando contenedor")
	#ret = dock.create_container(image="python:2.7", command='/bin/bash -c "ls; cd /appbuild; pip install pytest; pytest" ', volumes="/appbuild", name="build_00", host_config = dock.create_host_config(binds={"/home/matias/distri2/worker/build":{'bind':'/appbuild', 'mode':'rw'}}))
	
	ret = new_container("python:2.7")

	if ret:
		res = dock.start( ret['Id'] )
	
		print("[3] Ejecutando tests")
		dock.wait(ret['Id'])
		outpt = dock.logs(ret['Id'])

		fout = str(outpt)
		fout = fout.replace('\\n', '\n')
		fout = fout.replace('\\t', '\t')

		print(fout)

		print("[4] Parando contenedor")

		dock.stop( ret['Id'] )

		print("[5] Destruyendo contenedor")
		dock.remove_container( ret['Id'] )
	else:
		print("El lenguaje especificado no es soportado")

	if os.path.exists(os.path.join(os.getcwd(), "build")):
		os.system("rm -r build")



while True:
	job = beanstalk.reserve()
	print(job.body)
	make_build(job.body)
	job.delete()

