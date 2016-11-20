from appdata import db
from models import *


if __name__ == '__main__':
	db.create_all()
	db.session.add(User("admin", "admin"))
	db.session.add(User("worker", "qpzmalgd"))
	db.session.commit()

