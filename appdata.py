from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import beanstalkc

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

slack = slackweb.Slack(url="https://hooks.slack.com/services/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")

beanstalk = beanstalkc.Connection(host='beanstalk', port=11300)
