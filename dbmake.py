from appdata import db
from models import *


if __name__ == '__main__':
	db.create_all()
	db.session.add(Build("github.com/"))
	db.session.commit()

