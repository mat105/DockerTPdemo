from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime
from docker import Client

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

dockclient = Client(base_url='unix://var/run/docker.sock', version='auto')


class Build(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	path = db.Column(db.String(120))
	output = db.Column(db.Text)
	waiting = db.Column(db.Boolean)
	finished = db.Column(db.Boolean)
	date = db.Column(db.DateTime)

	def finish(bid):
		who = Build.query.filter_by(id=bid).first()
		who.finished = True
		db.session.commit()

	def bring():
		who = Build.query.filter_by(waiting=True).first()
		who.waiting = False
		db.session.commit()

	def jsonrep(self):
		return jsonify(hola=self.path)

	def __init__(self, path):
		self.path = path
		self.output = ""
		self.waiting = True
		self.finished = False
		self.date = datetime.utcnow()


@app.route('/create')
def creabd():
	db.create_all()
	db.session.add(Build("github.com/"))
	db.session.commit()
	return "hecho", 200

@app.route('/')
def hello_world():
	quer = Build.query.all()[0]
	return quer.jsonrep()

@app.route('/nuevo')
def nuevob():
	ret = dockclient.create_container(image="python:2", detach=True, command='/bin/bash -c "git clone https://github.com/mat105/GITPYTHONTESTS.git; pip install pytest; pytest" ')
	resp = dockclient.start( ret['Id'] ) 
	return str(dockclient.logs(ret['Id']))

@app.route('/hola')
def hello():
	return "holaquebuendia"


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=80, debug=True)

