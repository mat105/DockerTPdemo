from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import beanstalkc

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

beanstalk = beanstalkc.Connection(host='beanstalk', port=11300)
