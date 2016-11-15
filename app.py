from appdata import app, beanstalk
from models import Build

from flask import Response, jsonify, request
import json

@app.route('/')
def hello_world():
	return "Esto funciona", 200

@app.route('/build', methods=['POST'])
def init_build():
	path = "https://github.com/mat105/GITPYTHONTESTS.git" #request.form['path']

	build = Build("https://github.com/mat105/GITPYTHONTESTS.git")
	build.save()

	datosjson = {"id":build.id, "path":build.path }

	beanstalk.put(json.dumps(datosjson))

	return jsonify(build.id)

@app.route('/build/<int:build_id>', methods=['GET', 'PUT'])
def check_build(build_id):
	if request.method == 'GET':
		buildd = Build.query.filter_by(id=build_id).first()
	else:
		auth = request.authorization
		output = request.form['output']
		
		buildd = Build.query.filter_by(id=build_id).first()
		
		if buildd:
			if auth and auth.user == "worker" and auth.password == "123":
				buildd.update(output)
			else:
				return Response('Solo permitido a workers.\n'
				 'Necesita credenciales de autenticacion',
				 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

	if not buildd:
		return "Not found", 404

	return buildd.jsonrep()


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=80, debug=True)

