from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import beanstalkc
import slackweb
import logging



app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

slack = slackweb.Slack(url="https://hooks.slack.com/services/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")

beanstalk = beanstalkc.Connection(host='beanstalk', port=11300)


LOGGING_LEVEL = logging.INFO


logging.basicConfig(level=logging.INFO)


handler = logging.FileHandler('logs/api.log')
handler.setLevel(logging.INFO)

#handlerconsole = logging.StreamHandler(stream=sys.stdout)
#handlerconsole.setLevel(logging.INFO)

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
			#Logger.logger.addHandler(handlerconsole)

		return Logger.logger
