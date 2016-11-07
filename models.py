from appdata import db
from flask import jsonify

from datetime import datetime


class Build(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	path = db.Column(db.String(120))
	output = db.Column(db.Text)
	finished = db.Column(db.Boolean)
	date = db.Column(db.DateTime)

	def save(self):
		db.session.add(self)
		db.session.commit()

	def update(self, output):
		self.output = output
		self.finished = True

		db.session.commit()

	def jsonrep(self):
		return jsonify(repository=self.path, finished=self.finished, output=self.output)

	def __init__(self, path):
		self.path = path
		self.output = ""
		self.finished = False
		self.date = datetime.utcnow()
