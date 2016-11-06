from appdata import app, beanstalk
from models import Build


@app.route('/')
def hello_world():
	quer = Build.query.all()[0]
	return quer.jsonrep()


@app.route('/hola')
def hello():
	beanstalk.put("https://github.com/mat105/GITPYTHONTESTS.git")

	return "Procesada"


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=80, debug=True)

