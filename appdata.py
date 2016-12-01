from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import beanstalkc
#import slackweb
import logging

from config import LOGS_DIR

from flask.ext.httpauth import HTTPBasicAuth


#================================================

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

LOGS_DIR = 'logs/api.log'

beanstalk = beanstalkc.Connection(host='beanstalk', port=11300)

auth = HTTPBasicAuth()

#================================================

#slack = slackweb.Slack(url="https://hooks.slack.com/services/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")


logging.basicConfig(level=logging.INFO)


handler = logging.FileHandler(LOGS_DIR)
handler.setLevel(logging.INFO)

#================================================

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

class Logger:
	logger = None

	@staticmethod
	def get():
		if Logger.logger == None:
			Logger.logger = logging.getLogger(__name__)
			Logger.logger.setLevel(LOGGING_LEVEL)
			Logger.logger.addHandler(handler)

		return Logger.logger
