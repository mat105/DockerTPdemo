from appdata import app, beanstalk, slack, Logger
from models import Build, User

from flask import Response, jsonify, request, g
import json

from flask.ext.httpauth import HTTPBasicAuth


auth = HTTPBasicAuth()



@auth.verify_password
def verify_password(username, password):
	user = User.query.filter_by(name = username).first()
	
	if not user or not user.password == password:
		return False

	g.user = user
	return True


def slack_send(message):
    slack.notify(text=message)


@app.route('/')
def hello_world():
	return "Esto funciona", 200


order_translate = {
"date":Build.date,
"finished":Build.finished,
"path":Build.path
}

@app.route('/build', methods=['POST', 'GET'])
@auth.login_required
def init_build():
	if request.method == 'POST':
		path = request.form['path'] # "https://github.com/mat105/GITPYTHONTESTS.git"

		Logger.get().info("Pedido de testeo: %s" % (path,))

		build = Build(path, g.user)
		build.save()

		datosjson = {"id":build.id, "path":build.path }

		Logger.get().info("Agregando pedido a cola de mensajes")
		beanstalk.put(json.dumps(datosjson))
	else:
		orderby = request.args.get('order', 'date')
		orderformat = request.args.get('list', 'desc')

		filterpath = request.args.get('path', None)
		filterfinished = request.args.get('finished', None)
		
		orderby = order_translate.get(orderby, Build.date)

		if orderformat == 'desc':
			orderby = orderby.desc()

		builds = Build.query.filter_by(user_id=g.user.id)

		if filterpath:
			builds = builds.filter_by(path=filterpath)
		if filterfinished:
			builds = builds.filter_by(finished=filterfinished)

		builds = builds.order_by(orderby).all()
		results = []

		for bid in builds:
			results.append( bid.jsonrep(True) )

		return Response(json.dumps(results), mimetype="application/json")


	return jsonify(build.id)

@app.route('/build/<int:build_id>', methods=['GET', 'PUT'])
@auth.login_required
def check_build(build_id):
	if request.method == 'GET':
		Logger.get().info("Pedido de output del build n# %d por el usuario %s" % (build_id,g.user.name))
		buildd = Build.query.filter_by(id=build_id).first()

		if g.user.id != buildd.user.id:
			Logger.get().warning("Permisos denegados al usuario")
			return "Unauthorized", 401
			
	else:
		Logger.get().info("Pedido de actualizacion el build n# %d" % (build_id,))
		#auth = request.authorization
		output = request.form['output']
		
		buildd = Build.query.filter_by(id=build_id).first()
		
		if buildd:
			#if auth and auth.username == "worker" and auth.password == "123":
			if g.user.name == "worker":
				Logger.get().info("Actualizando")
				buildd.update(output)
				Logger.get().info("Notificando a slack")
				slack_send("Build %d terminado, repositorio %s" % (build_id, buildd.path))
			else:
				Logger.get().warning("Un usuario intenta modificar el build")

	if not buildd:
		return "Not found", 404

	return jsonify(buildd.jsonrep())


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=80, debug=True)

