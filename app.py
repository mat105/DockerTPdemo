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
		wha = Build.query.filter_by(id=build_id).first()
	else:
		output = request.form['output']
		
		wha = Build.query.filter_by(id=build_id).first()
		
		if wha:
			wha.update(output)

	return wha.jsonrep()


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=80, debug=True)

