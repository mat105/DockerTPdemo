import unittest
import app
import json

from base64 import b64enconde


class TestBuild(unittest.TestCase):
	
	def setUp(self):
		self.app = app.app.test_client()


	def tearDown(self):
		pass

	def test_new_build(self):
		headers = {
			'Authorization': 'Basic ' + b64encode("{0}:{1}".format('admin', 'admin'))
		}

		total_builds = self.app.get('/build', headers=headers)

		assert total_builds.statuscode == 200

		postbuild = self.app.post('/build', data={'path'='https://github.com/mat105/GITPYTHONTESTS.git'}, headers=headers)

		assert postbuild.statuscode == 200

		data = postbuild.get_json()

		assert data != None
		
		getbuild = self.app.get('/build/'+data['id'], headers=headers)

		assert getbuild.statuscode == 200

		data = getbuild.get_json()

		assert data != None

		assert data['finished'] == False


if __name__ == '__main__':
	unittest.main()
