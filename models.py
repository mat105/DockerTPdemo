from appdata import db
from flask import jsonify

from datetime import datetime


class Build(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	path = db.Column(db.String(120))
	output = db.Column(db.Text)
	finished = db.Column(db.Boolean)
	date = db.Column(db.DateTime)
	user = db.Column(db.String(40))

	def save(self):
		db.session.add(self)
		db.session.commit()

	def update(self, output):
		self.output = output
		self.finished = True

		db.session.commit()

	def jsonrep(self):
		return jsonify(repository=self.path, finished=self.finished, output=self.output)

	def __init__(self, path, user):
	    self.user = user
		self.path = path
		self.output = ""
		self.finished = False
		self.date = datetime.utcnow()
		
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), index=True)
    password = db.Column(db.String(16))
    
    @staticmethod
    def verify_auth_token(token):
        return None
        
    def verify_password(self, passwd):
        return passwd == self.password
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        
    def __init__(self, name, pwd):
        self.name = name
        self.password = pwd



