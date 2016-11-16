from appdata import app, beanstalk, slack
from models import Build, User

from flask import Response, jsonify, request
import json

from flask.ext.httpauth import HTTPBasicAuth


auth = HTTPBasicAuth()



@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(name = username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True



def slack_send(message):
    slack.notify(text=message)

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
			if auth and auth.username == "worker" and auth.password == "123":
				buildd.update(output)
				slack_send("Build %d terminado, repositorio %s" % (build_id, buildd.path))
			else:
				return Response('Solo permitido a workers.\n'
				 'Necesita credenciales de autenticacion',
				 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

	if not buildd:
		return "Not found", 404

	return buildd.jsonrep()


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=80, debug=True)

