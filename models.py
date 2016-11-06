from appdata import db
from flask import jsonify

from datetime import datetime


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
